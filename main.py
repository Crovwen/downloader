import os
from flask import Flask
from threading import Thread
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from handlers import start_handler, download_handler  # از پوشه handlers
import logging

# بارگذاری متغیرهای محیطی
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in environment variables!")

# فعال کردن لاگ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# ایجاد اپدیتور تلگرام
updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# هندلرها
dispatcher.add_handler(CommandHandler("start", start_handler.handle))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download_handler.handle))

# Flask برای زنده نگه داشتن
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

def run_bot():
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    Thread(target=run_flask).start()
    run_bot()
