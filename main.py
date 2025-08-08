from pyrogram import Client, filters
from pyrogram.types import Message
import re
import os
from handlers.link_handler import handle_link
from flask import Flask
import threading

BOT_TOKEN = "8431602847:AAGPz5QpBiwfVdi-2XPKif9abqxl_Uq7Cow"
API_ID = 20292726
API_HASH = "86902140c904c0de4a5813813c9a2409"

app_bot = Client(
    "auto_downloader_bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

@app_bot.on_message(filters.private | filters.group & filters.text)
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

# --- Flask app برای Render ---
server = Flask(__name__)

@server.route("/")
def home():
    return "Bot is running!"

def run_bot():
    app_bot.run()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 5000))
    server.run(host="0.0.0.0", port=port)
    
