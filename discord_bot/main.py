import discord
from discord.ext import commands, tasks
from core.hltv_scraper import get_upcoming_matches
from core.hltv_results import get_recent_hltv_results

import sys
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Setup intents and bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Allow imports from core/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.hltv_scraper import get_upcoming_matches
from core.prediction_manager import PredictionManager

predictions = PredictionManager()

@bot.event
async def on_ready():
    print(f"✅ Bot is ready: {bot.user}")
    check_results.start()

@bot.command()
async def matches(ctx):
    match_list = get_upcoming_matches()
    if not match_list:
        await ctx.send("⚠️ Couldn't fetch matches.")
        return
    msg = "\n".join([f"{i+1}. {m['team1']} vs {m['team2']} at {m['time']}" for i, m in enumerate(match_list)])
    await ctx.send(f"📅 Upcoming Matches:\n{msg}")


@bot.command()
async def predict(ctx, match_number: int, winner: str):
    match_list = get_upcoming_matches()
    try:
        match = match_list[match_number - 1]

        # Save match info for later result checking
        match_info = {
            "team1": match['team1'],
            "team2": match['team2'],
            "time": match['time'],  # ISO 8601 timestamp from PandaScore
        }

        predictions.add_prediction(str(ctx.author.id), match['match_id'], winner, match_info)

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

@tasks.loop(minutes=10)
async def check_results():
    hltv_results = get_recent_hltv_results()

    for user_id, match_id, predicted in predictions.get_predictions():
        match_info = predictions.get_match_info(match_id)
        
        for result in hltv_results:
            if (
                predicted.lower() in [result['team1'].lower(), result['team2'].lower()]
                and match_info['team1'].lower() in [result['team1'].lower(), result['team2'].lower()]
                and match_info['team2'].lower() in [result['team1'].lower(), result['team2'].lower()]
                and abs((result['timestamp'] - match_info['time']).total_seconds()) < 6 * 3600  # ±6 hrs window
            ):
                # Score is like "16-12", extract winner
                winner = result['team1'] if int(result['score'].split('-')[0]) > int(result['score'].split('-')[1]) else result['team2']

                user = await bot.fetch_user(int(user_id))
                if predicted.lower() == winner.lower():
                    predictions.increment_score(user_id)
                    await user.send(f"✅ Correct prediction: {winner}")
                else:
                    await user.send(f"❌ Wrong prediction: {winner} won")
                predictions.delete_prediction(user_id, match_id)
                break

bot.run(TOKEN)
