from instagrapi import Client

cl = Client()
cl.load_settings("cookie.json")  # فایل کوکی کنار main.py

# تست اتصال
me = cl.account_info()
print("ورود موفق ✅", me.username)

import os
from threading import Thread
from flask import Flask
from pyrogram import Client, filters
import asyncio

# ایمپورت هندلر لینک‌ها
from handlers import link_handler

# ثابت‌های بات
API_ID = 20292726
API_HASH = "86902140c904c0de4a5813813c9a2409"
BOT_TOKEN = "8431602847:AAFqNrL2wUPY_4hlUUCMLAuek0qlb5DC9BQ"

# ساخت کلاینت Pyrogram
bot = Client(
    "downloader_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# دستور start
@bot.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text("سلام 👋\nلینک رو بفرست تا برات دانلود کنم 📥")

# دریافت لینک و ارسال به link_handler
@bot.on_message(filters.text & ~filters.command("start"))
async def link_receiver(client, message):
    url = message.text.strip()
    await link_handler.handle_link(client, message, url)

# Flask برای زنده نگه داشتن
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

def run_bot():
    bot.run()

if __name__ == "__main__":
    Thread(target=run_flask).start()
    run_bot()
