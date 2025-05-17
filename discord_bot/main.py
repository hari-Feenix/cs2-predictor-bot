import discord
from discord.ext import commands, tasks
from core.hltv_scraper import get_upcoming_matches
from core.prediction_manager import PredictionManager

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Setup Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Manage predictions
predictions = PredictionManager()

@bot.event
async def on_ready():
    print(f"✅ Bot is online: {bot.user}")
    check_results.start()

@bot.command()
async def matches(ctx):
    match_list = get_upcoming_matches()
    if not match_list:
        await ctx.send("⚠️ Couldn't fetch matches.")
        return
    msg = "\n".join([f"{i+1}. {m['team1']} vs {m['team2']} at {m['time']}" for i, m in enumerate(match_list)])
    await ctx.send(f"📅 **Upcoming Matches:**\n{msg}")

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
    await ctx.send(f"🏆 **Leaderboard:**\n{msg}")

@bot.command()
async def checknow(ctx):
    await ctx.send("🔄 Results check triggered manually.")
    await check_results_function()

@bot.command()
async def results(ctx):
    from core.hltv_scraper import get_recent_results
    await ctx.send("📊 Fetching recent results...")

    try:
        results = get_recent_results()
        if not results:
            await ctx.send("⚠️ No recent results found.")
            return

        msg = "\n".join([f"{r['team1']} {r['score1']} - {r['score2']} {r['team2']}" for r in results])
        await ctx.send(f"📈 Recent Match Results:\n{msg}")

    except Exception as e:
        await ctx.send("❌ Error while fetching results.")
        print(f"[ERROR] Results command failed: {e}")


@tasks.loop(minutes=10)
async def check_results():
    await check_results_function()

async def check_results_function():
    dummy_results = {
        # Placeholder logic: replace with real fetch logic later
        'NAVI_vs_Vitality_1715880000': 'NAVI'
    }
    for user_id, match_id, predicted in predictions.get_predictions():
        if match_id in dummy_results:
            actual = dummy_results[match_id]
            user = await bot.fetch_user(int(user_id))
            if predicted.lower() == actual.lower():
                predictions.increment_score(user_id)
                await user.send(f"✅ Correct prediction: {actual}")
            else:
                await user.send(f"❌ Wrong prediction: {actual} won")
            predictions.delete_prediction(user_id, match_id)

bot.run(TOKEN)
