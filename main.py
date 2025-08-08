from pyrogram import Client, filters
from pyrogram.types import Message
import re
from handlers.link_handler import handle_link

# توکن مستقیم داخل کد
BOT_TOKEN = "8431602847:AAGPz5QpBiwfVdi-2XPKif9abqxl_Uq7Cow"

# استفاده از session موقتی تا Pyrogram دنبال user session قدیمی نگرده
app = Client(
    name=":memory:",  # بدون ذخیره‌سازی session در فایل
    bot_token=BOT_TOKEN
)

@app.on_message((filters.private | filters.group) & filters.text)
async def on_message(client: Client, message: Message):
    urls = re.findall(r'(https?://[^\s]+)', message.text or "")
    if not urls:
        return
    for url in urls:
        await message.reply_chat_action("upload_document")
        await handle_link(client, message, url)

@app.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    await message.reply(
        "سلام!\n"
        "کافیه لینک هر فایل، ویدیو، موزیک یا هر محتوایی که میخوای دانلود کنی رو اینجا بفرستی، من برات می‌فرستم.\n"
        "از لینک‌های تلگرام پشتیبانی نمی‌کنم.\n"
        "با من همراه باش 🚀"
    )

if __name__ == "__main__":
    app.run()
