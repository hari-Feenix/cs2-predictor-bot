import discord
from discord.ext import commands, tasks
from hltv_scraper import get_upcoming_matches
from prediction_manager import PredictionManager

TOKEN = 'YOUR_DISCORD_BOT_TOKEN'

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

predictions = PredictionManager()

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')
    check_results.start()

@bot.command()
async def matches(ctx):
    match_list = get_upcoming_matches()
    msg = "\n".join([f"{i+1}. {m['team1']} vs {m['team2']} at {m['time']}" for i, m in enumerate(match_list[:5])])
    await ctx.send(f"Upcoming Matches:\n{msg}")

@bot.command()
async def predict(ctx, match_number: int, winner: str):
    match_list = get_upcoming_matches()
    try:
        match = match_list[match_number - 1]
        predictions.add_prediction(ctx.author.id, match['match_id'], winner)
        await ctx.send(f"Prediction saved: {winner} wins in {match['team1']} vs {match['team2']}")
    except IndexError:
        await ctx.send("Invalid match number.")

@tasks.loop(minutes=10)
async def check_results():
    await predictions.update_results(bot)

bot.run(TOKEN)
