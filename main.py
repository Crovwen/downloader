import os
import threading
from flask import Flask
from bot import run_bot  # اینو از bot.py می‌گیریم
from dotenv import load_dotenv

# لود کردن متغیرها از .env
load_dotenv()

# Flask برای باز نگه داشتن پورت در Render
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

if __name__ == "__main__":
    # استارت بات در یک Thread جدا
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

    # ران کردن Flask
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
