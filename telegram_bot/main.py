import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)
from core.hltv_scraper import get_upcoming_matches
from core.prediction_manager import PredictionManager

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

predictions = PredictionManager()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to the CS2 Predictor Bot!")

async def matches(update: Update, context: ContextTypes.DEFAULT_TYPE):
    match_list = get_upcoming_matches()[:5]
    buttons = []
    for i, m in enumerate(match_list):
        match_text = f"{m['team1']} vs {m['team2']} at {m['time']}"
        btns = [
            InlineKeyboardButton(m['team1'], callback_data=f"{m['match_id']}|{m['team1']}"),
            InlineKeyboardButton(m['team2'], callback_data=f"{m['match_id']}|{m['team2']}")
        ]
        buttons.append([btns[0], btns[1]])
        await update.message.reply_text(match_text, reply_markup=InlineKeyboardMarkup([btns]))

async def handle_prediction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = str(query.from_user.id)
    match_id, team = query.data.split('|')
    predictions.add_prediction(user_id, match_id, team)
    await query.edit_message_text(f"✅ Prediction saved: {team} to win match {match_id}")

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    board = predictions.get_leaderboard()
    text = "\n".join([f"{uid}: {score} pts" for uid, score in board])
    await update.message.reply_text(f"🏆 Leaderboard:\n{text or 'No data yet.'}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("matches", matches))
    app.add_handler(CommandHandler("leaderboard", leaderboard))
    app.add_handler(CallbackQueryHandler(handle_prediction))

    print("🤖 Telegram bot is running...")
    app.run_polling()
