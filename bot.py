import os
from pyrogram import Client, filters
from dotenv import load_dotenv

# لود کردن توکن از .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

app = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
def start_cmd(client, message):
    message.reply_text("✅ Bot is alive and working!")

def run_bot():
    app.run()
  
