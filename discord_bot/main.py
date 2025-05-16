import discord
from discord.ext import commands, tasks
import os
import sys
from dotenv import load_dotenv

# Extend path to include core directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'core')))

# Import logic modules
from hltv_scraper import get_upcoming_matches
from prediction_manager import PredictionManager

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Initialize bot with message content intent
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Initialize prediction manager
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
    except Exception as e:
        await ctx.send(f"⚠️ Error saving prediction: {e}")

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
    await ctx.send("🧪 Results check triggered manually.")
    await perform_result_check()

@tasks.loop(minutes=10)
async def check_results():
    await perform_result_check()

async def perform_result_check():
    # Replace with real result mapping logic in production
    dummy_results = {
        '123456': 'Team A',
        '789012': 'Team B'
    }
    for user_id, match_id, predicted in predictions.get_predictions():
        if match_id in dummy_results:
            actual = dummy_results[match_id]
            try:
                user = await bot.fetch_user(int(user_id))
                if predicted.lower() == actual.lower():
                    predictions.increment_score(user_id)
                    await user.send(f"✅ Correct prediction: {actual}")
                else:
                    await user.send(f"❌ Wrong prediction: {actual} won.")
                predictions.delete_prediction(user_id, match_id)
            except Exception as e:
                print(f"⚠️ Failed to notify user {user_id}: {e}")

bot.run(TOKEN)
