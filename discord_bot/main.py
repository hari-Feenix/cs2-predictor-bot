import discord
from discord.ext import commands, tasks
from core.hltv_scraper import get_upcoming_matches

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

@tasks.loop(minutes=10)
async def check_results():
    print("🔍 Checking results from Pandascore...")

    headers = {
        "Authorization": f"Bearer {os.getenv('PANDASCORE_API_KEY')}"
    }

    for user_id, match_id, predicted in predictions.get_predictions():
        try:
            url = f"https://api.pandascore.co/csgo/matches/{match_id}"
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"Failed to fetch result for match {match_id}")
                continue

            data = response.json()

            # Only check completed matches
            if data["status"] != "finished" or not data.get("winner"):
                continue

            actual_winner = data["winner"]["name"]
            user = await bot.fetch_user(int(user_id))

            if predicted.lower() == actual_winner.lower():
                predictions.increment_score(user_id)
                await user.send(f"✅ Correct prediction! {actual_winner} won match ID {match_id}. 🎯")
            else:
                await user.send(f"❌ Wrong prediction! Actual winner was {actual_winner}.")

            predictions.delete_prediction(user_id, match_id)

        except Exception as e:
            print(f"Error processing result for match {match_id}: {e}")

bot.run(TOKEN)
