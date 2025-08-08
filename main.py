import threading
from flask import Flask
from pyrogram import Client, filters

# ======== تنظیمات Pyrogram ========
API_ID = 20292726
API_HASH = "86902140c904c0de4a5813813c9a2409"
BOT_TOKEN = "8431602847:AAGPz5QpBiwfVdi-2XPKif9abqxl_Uq7Cow"

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_bot():
    app_bot = Client(
        "downloader_bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN
    )

    @app_bot.on_message(filters.command("start"))
    async def start_cmd(client, message):
        await message.reply("سلام! لینک رو بفرست تا دانلود کنم.")

    app_bot.run()

if __name__ == "__main__":
    # اجرای بات توی ترد جدا
    threading.Thread(target=run_bot).start()
    # اجرای Flask روی Render
    app.run(host="0.0.0.0", port=10000)
