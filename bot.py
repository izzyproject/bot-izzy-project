import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("VIRTUSIM_API_KEY")
API_URL = "https://virtusim.com/api/json.php"

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN tidak ditemukan di .env")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Bot Virtusim siap 🚀\nKetik /order untuk mulai.")

async def order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    payload = {
        "api_key": API_KEY,
        "action": "order",
        "service": "26",        # ID layanan
        "operator": "indosat"   # atau telkomsel, axis, dll
    }
    response = requests.post(API_URL, data=payload)
    result = response.text
    await update.message.reply_text(f"📦 Order response:\n{result}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("order", order))

if __name__ == "__main__":
    print("Bot running...")
    app.run_polling()
