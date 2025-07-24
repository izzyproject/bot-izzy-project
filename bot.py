import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests

BOT_TOKEN = os.getenv("TOKEN")
VIRTUSIM_APIKEY = os.getenv("VIRTUSIM_APIKEY")

# Logging
logging.basicConfig(level=logging.INFO)

# Command /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Kirim nomor untuk beli kuota.")

# Command /order contoh
async def order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Contoh: /order 6281234567890")

    nomor = context.args[0]
    try:
        response = requests.post("https://api.virtusim.com/order", json={
            "phone": nomor
        }, headers={
            "Authorization": f"Bearer {VIRTUSIM_APIKEY}"
        })

        data = response.json()
        if data.get("success"):
            await update.message.reply_text(f"✅ Order sukses: {data}")
        else:
            await update.message.reply_text(f"❌ Gagal: {data.get('message')}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# Main app
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("order", order))

    print("Bot is running...")
    app.run_polling()
