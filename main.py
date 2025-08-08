import os
import asyncio
from flask import Flask
from threading import Thread
from pyrogram import Client, filters
from dotenv import load_dotenv

# Load env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

# Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

# Pyrogram client
bot = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@bot.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    await message.reply_text("✅ Bot is alive and working!")

# Function to run the bot in asyncio loop
async def run_bot():
    await bot.start()
    print("Bot started...")
    await asyncio.Event().wait()  # Keep running

def start_bot():
    asyncio.run(run_bot())

if __name__ == "__main__":
    # Start bot in separate thread
    Thread(target=start_bot, daemon=True).start()

    # Start Flask server
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
