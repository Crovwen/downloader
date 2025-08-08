#!/usr/bin/env python3
# bot_runner.py
import os
import re
from pyrogram import Client, filters
from handlers.link_handler import handle_link
from pyrogram.types import Message

# ---------- تنظیمات (مقداردهی مستقیم داخل کد) ----------
API_ID = 20292726
API_HASH = "86902140c904c0de4a5813813c9a2409"
BOT_TOKEN = "8431602847:AAGPz5QpBiwfVdi-2XPKif9abqxl_Uq7Cow"
# --------------------------------------------------------

app = Client(
    "downloader_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workdir=os.path.dirname(__file__)  # مطمئن می‌شه session/cache محلی باشه
)

@app.on_message((filters.private | filters.group) & filters.text)
async def on_message(client: Client, message: Message):
    try:
        text = message.text or ""
        urls = re.findall(r'(https?://[^\s]+)', text)
        if not urls:
            return
        for url in urls:
            # به کاربر وضعیت میدیم و سپس هندلر لینک رو صدا می‌زنیم
            try:
                await message.reply_chat_action("upload_document")
            except:
                pass
            await handle_link(client, message, url)
    except Exception as e:
        # جلوگیری از کرش کلی بات به خاطر خطا در هندلر
        try:
            await message.reply(f"⚠️ خطا در پردازش لینک: {e}")
        except:
            print("Error while replying to user:", e)

@app.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    await message.reply(
        "✅ ربات دانلودر فعال است!\n"
        "لینک فایل/ویدیو/موزیک یا هر موردی که می‌خوای دانلود بشه رو اینجا بفرست."
    )

if __name__ == "__main__":
    print("[BOT] bot_runner starting...")
    # اینجا Pyrogram در پروسس خودش اجرا میشه (main thread) — امن و پایدار
    app.run()
  
