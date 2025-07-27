from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import logging

# 🔐 توکن ربات پشتیبانی
TOKEN = '7988090486:AAEFF4WIUJ0tak3TN_5-XQcJooYFHBUIC7g'
# 🧑‍💼 آی‌دی عددی ادمین (تلگرام)
ADMIN_ID = 5095867558

# ذخیره پیام‌ها برای ارتباط پیام-کاربر
user_messages = {}

# لاگ‌ها
logging.basicConfig(level=logging.INFO)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛠️ Welcome to Support!\nPlease describe your issue, and we will respond shortly.")

# دریافت پیام کاربر
async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = update.message

    # ذخیره پیام کاربر برای ارسال پاسخ از ادمین
    user_messages[msg.message_id] = user.id

    # ارسال به ادمین
    text = f"📩 New message from {user.full_name} (@{user.username} | ID: {user.id}):\n\n{msg.text}"
    sent = await context.bot.send_message(chat_id=ADMIN_ID, text=text)
    # پیام ارسالی رو به آی‌دی پیام کاربر مپ کن
    user_messages[sent.message_id] = user.id

# ریپلای ادمین به پیام
async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    # فقط ادمین اجازه داره
    if update.effective_user.id != ADMIN_ID:
        return

    if msg.reply_to_message and msg.reply_to_message.message_id in user_messages:
        user_id = user_messages[msg.reply_to_message.message_id]
        try:
            await context.bot.send_message(chat_id=user_id, text=f"💬 Support Reply:\n{msg.text}")
            await msg.reply_text("✅ Reply sent to user.")
        except:
            await msg.reply_text("❌ Failed to send message to user.")
    else:
        await msg.reply_text("❗ Please reply to a user's message to respond.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.User(user_id=ADMIN_ID), admin_reply))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.User(user_id=ADMIN_ID), handle_user_message))
    app.run_polling()

if __name__ == "__main__":
    main()
