import discord
from discord.ext import commands, tasks
import os
import sys
from dotenv import load_dotenv

# Allow access to core module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.hltv_scraper import get_upcoming_matches, fetch_recent_results
from core.prediction_manager import PredictionManager

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Prediction tracking
predictions = PredictionManager()

@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")
    check_results.start()

@bot.command()
async def matches(ctx):
    match_list = get_upcoming_matches()
    if not match_list:
        await ctx.send("⚠️ Couldn't fetch matches.")
        return

    msg = "\n".join([
        f"{i+1}. {m['team1']} vs {m['team2']} at {m['time']}"
        for i, m in enumerate(match_list)
    ])
    await ctx.send(f"📅 Upcoming Matches:\n{msg}")

@bot.command()
async def predict(ctx, match_number: int, winner: str):
    match_list = get_upcoming_matches()
    try:
        match = match_list[match_number - 1]
        predictions.add_prediction(str(ctx.author.id), match['match_id'], winner)
        await ctx.send(f"✅ Prediction saved: {winner} wins in {match['team1']} vs {match['team2']}")
    except IndexError:
        await ctx.send("❌ Invalid match number.")

@bot.command()
async def leaderboard(ctx):
    leaders = predictions.get_leaderboard()
    if not leaders:
        await ctx.send("📉 No leaderboard data yet.")
        return

    msg = "\n".join([f"<@{uid}> - {score} pts" for uid, score in leaders])
    await ctx.send(f"🏆 Leaderboard:\n{msg}")

@bot.command()
async def checknow(ctx):
    await ctx.send("🔄 Results check triggered manually.")
    await process_results()

@tasks.loop(minutes=10)
async def check_results():
    await process_results()

async def process_results():
    results = fetch_recent_results()
    if not results:
        return

    for user_id, match_id, predicted in predictions.get_predictions():
        if match_id in results:
            actual_winner = results[match_id]['winner']
            user = await bot.fetch_user(int(user_id))

            if predicted.lower() == actual_winner.lower():
                predictions.increment_score(user_id)
                await user.send(f"✅ Correct prediction! {actual_winner} won.")
            else:
                await user.send(f"❌ Wrong prediction. {actual_winner} won.")
            predictions.delete_prediction(user_id, match_id)

# Run the bot
bot.run(TOKEN)
