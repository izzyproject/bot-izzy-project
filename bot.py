import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Ambil dari environment (Render)
BOT_TOKEN = os.getenv("8245152079:AAHX_glLG7k2GuTLzu1hgTDXQAg2DuVUBbM")
VIRTUSIM_APIKEY = os.getenv("q20QeJ3PjsxAyYCSF6BRNvHI9agX4U")  # ← pastikan ini juga diset di Environment

# Cek token
if not BOT_TOKEN:
    raise ValueError("❌ TOKEN tidak ditemukan!")
if not VIRTUSIM_APIKEY:
    raise ValueError("❌ VIRTUSIM_APIKEY tidak ditemukan!")

# Init app
app = ApplicationBuilder().token(BOT_TOKEN).build()


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Selamat datang di Bot Virtusim.\nKetik /produk untuk melihat daftar.")


# /produk → ambil produk dari API Virtusim
async def produk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = f"https://api.virtusim.com/api/product?api_key={VIRTUSIM_APIKEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if data["status"] == True:
            msg = "📦 *Daftar Produk:*\n"
            for item in data["data"][:10]:  # tampilkan 10 produk pertama
                msg += f"\n🔹 ID: `{item['id']}`\n📱 {item['name']}\n💰 {item['price']} {item['currency']}\n"
            await update.message.reply_text(msg, parse_mode="Markdown")
        else:
            await update.message.reply_text("Gagal mengambil produk.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error ambil produk: {e}")


# /order <id_produk>
async def order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 1:
        await update.message.reply_text("⚠️ Format salah!\nContoh: /order 421")
        return

    product_id = args[0]
    phone_number = "6281234567890"  # Ganti ini nanti pakai input user

    url = f"https://api.virtusim.com/api/order"
    payload = {
        "api_key": VIRTUSIM_APIKEY,
        "product_id": product_id,
        "phone_number": phone_number
    }

    try:
        response = requests.post(url, json=payload)
        data = response.json()
        if data.get("status") == True:
            detail = data.get("data", {})
            await update.message.reply_text(
                f"✅ Order Berhasil!\n\n📱 Produk: {detail.get('product_name')}\n📞 Nomor: {detail.get('phone_number')}\n🆔 Order ID: {detail.get('order_id')}"
            )
        else:
            await update.message.reply_text(f"❌ Gagal Order: {data.get('message')}")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error order: {e}")


# Handler
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("produk", produk))
app.add_handler(CommandHandler("order", order))

# Run
if __name__ == '__main__':
    print("🤖 Bot Virtusim aktif...")
    app.run_polling()
