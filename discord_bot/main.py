import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from core.hltv_scraper import get_upcoming_matches
from core.prediction_manager import PredictionManager

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
predictions = PredictionManager()

@bot.event
async def on_ready():
    print(f'✅ Bot connected as {bot.user}')
    check_results.start()

@bot.command()
async def matches(ctx):
    match_list = get_upcoming_matches()
    msg = "\n".join([f"{i+1}. {m['team1']} vs {m['team2']} at {m['time']}" for i, m in enumerate(match_list[:5])])
    await ctx.send(f"📅 Upcoming Matches:\n{msg}")

@bot.command()
async def predict(ctx, match_number: int, winner: str):
    match_list = get_upcoming_matches()
    try:
        match = match_list[match_number - 1]
        predictions.add_prediction(ctx.author.id, match['match_id'], winner)
        await ctx.send(f"✅ Prediction saved: {winner} wins in {match['team1']} vs {match['team2']}")
    except IndexError:
        await ctx.send("❌ Invalid match number.")

@bot.command()
async def leaderboard(ctx):
    board = predictions.get_leaderboard()
    msg = "\n".join([f"<@{uid}>: {score} pts" for uid, score in board])
    await ctx.send(f"🏆 Leaderboard:\n{msg}")

@tasks.loop(minutes=10)
async def check_results():
    await predictions.update_results(bot)

bot.run(TOKEN)
