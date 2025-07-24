from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import requests
import os

# Step percakapan
CHOOSE_APP, GET_PHONE = range(2)

# API Key Virtusim dari environment
API_KEY = os.getenv("q20QeJ3PjsxAyYCSF6BRNvHI9agX4U")

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['WhatsApp', 'Instagram'], ['Gmail', 'Facebook']]
    await update.message.reply_text(
        "Selamat datang! Pilih aplikasi OTP yang ingin kamu beli:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    )
    return CHOOSE_APP

# Pilih aplikasi
async def choose_app(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['app'] = update.message.text
    await update.message.reply_text("Masukkan nomor HP tujuan:")
    return GET_PHONE

# Proses pembelian
async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text
    app = context.user_data['app'].lower().replace("+", "").replace(" ", "")
    url = f"https://virtusim.com/api/order?api_key={API_KEY}&nomor={phone}&produk={app}"

    try:
        response = requests.get(url).json()
        if response.get("status") == "success":
            await update.message.reply_text(f"✅ Order berhasil!\nNomor: {phone}\nAplikasi: {app}")
        else:
            await update.message.reply_text(f"❌ Gagal order. Info: {response}")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")

    return ConversationHandler.END

# Main function
def main():
    token = os.getenv("8245152079:AAHX_glLG7k2GuTLzu1hgTDXQAg2DuVUBbM")
    app = ApplicationBuilder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSE_APP: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_app)],
            GET_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        },
        fallbacks=[]
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
