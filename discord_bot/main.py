import discord
from discord.ext import commands, tasks
import sys
import os
from dotenv import load_dotenv

# Setup environment
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Setup bot with message content intent
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Ensure core modules can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.hltv_scraper import get_upcoming_matches
from core.prediction_manager import PredictionManager

# Prediction manager instance
predictions = PredictionManager()

@bot.event
async def on_ready():
    print(f"Bot is ready: {bot.user}")
    check_results.start()

@bot.command()
async def matches(ctx):
    match_list = get_upcoming_matches()
    if not match_list:
        await ctx.send("⚠️ Couldn't fetch matches.")
        return
    msg = "\n".join([f"{i+1}. {m['team1']} vs {m['team2']} at {m['time']}" for i, m in enumerate(match_list[:5])])
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
        await ctx.send("No leaderboard data yet.")
        return
    msg = "\n".join([f"<@{uid}> - {score} pts" for uid, score in leaders])
    await ctx.send(f"🏆 Leaderboard:\n{msg}")

@tasks.loop(minutes=10)
async def check_results():
    # Dummy placeholder until real results are implemented
    dummy_results = {
        '123456': 'Team A',
        '789012': 'Team B'
    }
    for user_id, match_id, predicted in predictions.get_predictions():
        if match_id in dummy_results:
            actual = dummy_results[match_id]
            user = await bot.fetch_user(int(user_id))
            if predicted == actual:
                predictions.increment_score(user_id)
                await user.send(f"✅ Correct prediction: {actual}")
            else:
                await user.send(f"❌ Wrong prediction: {actual} won")
            predictions.delete_prediction(user_id, match_id)

bot.run(TOKEN)
