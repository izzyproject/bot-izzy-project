import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import requests

BOT_TOKEN = os.environ.get("BOT_TOKEN")
VIRTUSIM_API_KEY = os.environ.get("VIRTUSIM_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Selamat datang! Ketik /order untuk melakukan pembelian.")

async def order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone_number = "6281234567890"  # Ganti sesuai kebutuhan
    product_code = "XLSAKTI10"      # Contoh kode produk

    url = "https://api.virtusim.com/api/v1/order"
    headers = {
        "Authorization": f"Bearer {VIRTUSIM_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "buyer_sku_code": product_code,
        "customer_no": phone_number,
        "ref_id": "order12345"
    }

    response = requests.post(url, json=payload, headers=headers)
    result = response.json()

    if result.get("status") == True:
        await update.message.reply_text(f"Sukses! Pesanan: {result['message']}")
    else:
        await update.message.reply_text(f"Gagal! {result.get('message', 'Terjadi kesalahan.')}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("order", order))

if __name__ == "__main__":
    app.run_polling()
