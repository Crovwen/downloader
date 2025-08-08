import asyncio
import threading
import os
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message
import re
from handlers.link_handler import handle_link

API_ID = 20292726
API_HASH = "86902140c904c0de4a5813813c9a2409"
BOT_TOKEN = "8431602847:AAGPz5QpBiwfVdi-2XPKif9abqxl_Uq7Cow"

app_bot = Client(
    "auto_downloader_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# --- Bot Handlers ---
@app_bot.on_message(filters.private | (filters.group & filters.text))
async def on_message(client: Client, message: Message):
    urls = re.findall(r'(https?://[^\s]+)', message.text or "")
    if not urls:
        return
    for url in urls:
        await message.reply_chat_action("upload_document")
        await handle_link(client, message, url)

@app_bot.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    await message.reply(
        "سلام!\n"
        "کافیه لینک هر فایل، ویدیو، موزیک یا هر محتوایی که میخوای دانلود کنی رو اینجا بفرستی، من برات می‌فرستم.\n"
        "از لینک‌های تلگرام پشتیبانی نمی‌کنم.\n"
        "با من همراه باش 🚀"
    )

# --- Flask App ---
app_web = Flask(__name__)

@app_web.route("/")
def home():
    return "Bot is running!", 200

# --- Run Flask in a separate thread ---
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port)

# --- Async main to start bot ---
async def main():
    await app_bot.start()
    print("Bot started ✅")
    await asyncio.Event().wait()  # Keep running forever

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    asyncio.run(main())
