import threading
from flask import Flask
from pyrogram import Client, filters, idle

# ======== تنظیمات Pyrogram ========
API_ID = 20292726
API_HASH = "86902140c904c0de4a5813813c9a2409"
BOT_TOKEN = "import threading
from flask import Flask
from pyrogram import Client, filters, idle

# ======== تنظیمات Pyrogram ========
API_ID = 20292726
API_HASH = "86902140c904c0de4a5813813c9a2409"
BOT_TOKEN = "8431602847:AAGPz5QpBiwfVdi-2XPKif9abqxl_Uq7Cow"

# Flask برای نگه داشتن سرویس روی Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run_bot():
    bot = Client(
        "my_downloader_bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN
    )

    @bot.on_message(filters.command("start"))
    async def start_cmd(client, message):
        await message.reply("✅ ربات فعال است!\nلینک یا فایل خود را ارسال کنید.")

    bot.start()
    idle()
    bot.stop()

if __name__ == "__main__":
    # اجرای بات در ترد جدا
    threading.Thread(target=run_bot, daemon=True).start()

    # اجرای Flask روی پورت Render
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)"

# Flask برای نگه داشتن سرویس روی Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run_bot():
    bot = Client(
        "my_downloader_bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN
    )

    @bot.on_message(filters.command("start"))
    async def start_cmd(client, message):
        await message.reply("✅ ربات فعال است!\nلینک یا فایل خود را ارسال کنید.")

    bot.start()
    idle()
    bot.stop()

if __name__ == "__main__":
    # اجرای بات در ترد جدا
    threading.Thread(target=run_bot, daemon=True).start()

    # اجرای Flask روی پورت Render
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
