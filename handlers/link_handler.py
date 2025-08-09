import os
import re
import logging
from urllib.parse import urlparse

from services.youtube import download_youtube
from services.instagram import download_instagram
from services.tiktok import download_tiktok
from services.pinterest import download_pinterest
from services.soundcloud import download_soundcloud
from services.spotify import download_spotify
from services.google_drive import download_google_drive
from services.mediafire import download_mediafire
from services.dropbox import download_dropbox
from services.generic_downloader import download_direct_link

# تنظیم لاگ (اگر در جای دیگری لاگ تنظیم شده باشه این خط ایمن است)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# regex برای پیدا کردن اولین URL در متن (ساده و قابل اعتماد برای بیشتر موارد)
URL_RE = re.compile(
    r'((?:https?://)?(?:www\.)?[^\s/$.?#].[^\s]*)',
    flags=re.IGNORECASE
)

async def handle_link(client, message, raw_text):
    """
    ورودی:
      client: pyrogram client
      message: pyrogram message
      raw_text: متن دریافتی از کاربر (ممکنه حاوی url باشد)
    رفتار:
      - اولین URL را استخراج می‌کند
      - تشخیص می‌دهد چه سرویسی باید استفاده شود
      - تلاش برای دانلود با تابع مخصوص
      - در صورت خطا یکبار fallback به دانلود مستقیم می‌کند
      - فقط یک پیام خطا به کاربر می‌دهد (بدون تکرار)
    """
    # استخراج اولین url
    match = URL_RE.search(raw_text.strip())
    if not match:
        await message.reply("❌ لینک معتبر پیدا نشد. لطفاً یک لینک صحیح بفرست.")
        return

    url = match.group(1).strip()

    # اگر schema نداشت، سعی می‌کنیم http:// بهش اضافه کنیم
    if not urlparse(url).scheme:
        url = "https://" + url

    domain = urlparse(url).netloc.lower()
    logger.info("Received URL: %s (domain: %s) from chat %s", url, domain, message.chat.id)

    # جلوگیری از پردازش لینک‌های تلگرام
    if "t.me" in domain or "telegram" in domain:
        await message.reply("❌ متأسفانه پشتیبانی از لینک‌های تلگرام انجام نمی‌شود.")
        return

    file_path = None
    gave_user_message = False  # برای جلوگیری از پیام تکراری به کاربر

    # map دامنه -> تابع دانلود (تابع‌ها فرض شده async و فایل مسیر محلی برمی‌گردانند یا None)
    try:
        if any(x in domain for x in ["youtube.com", "youtu.be"]):
            logger.info("Using youtube downloader for %s", url)
            file_path = await download_youtube(url)

        elif "instagram.com" in domain or "instagr.am" in domain:
            logger.info("Using instagram downloader for %s", url)
            try:
                file_path = await download_instagram(url)
            except Exception as e:
                # پیام مشخص برای نیاز به لاگین/کوکی
                msg = str(e).lower()
                if "need to log in" in msg or "cookies" in msg or "login" in msg:
                    await message.reply("⚠️ این لینک اینستاگرام ممکن است نیاز به ورود به حساب (کوکی) داشته باشد. بدون کوکی بعضی محتواها دانلود نمی‌شوند.")
                    gave_user_message = True
                    # ادامه می‌دهیم تا fallback انجام بشه
                else:
                    logger.exception("instagram downloader error for %s", url)
                    # اجازه می‌دهیم که fallback انجام شود

        elif "tiktok.com" in domain or "vm.tiktok.com" in domain:
            logger.info("Using tiktok downloader for %s", url)
            file_path = await download_tiktok(url)

        elif "pinterest.com" in domain:
            logger.info("Using pinterest downloader for %s", url)
            try:
                file_path = await download_pinterest(url)
            except Exception as e:
                logger.exception("pinterest downloader error for %s", url)
                # اجازه می‌دهیم fallback انجام شود

        elif "soundcloud.com" in domain:
            logger.info("Using soundcloud downloader for %s", url)
            file_path = await download_soundcloud(url)

        elif "spotify.com" in domain:
            logger.info("Using spotify downloader for %s", url)
            file_path = await download_spotify(url)

        elif any(x in domain for x in ["drive.google.com", "docs.google.com"]):
            logger.info("Using google drive downloader for %s", url)
            file_path = await download_google_drive(url)

        elif "mediafire.com" in domain:
            logger.info("Using mediafire downloader for %s", url)
            file_path = await download_mediafire(url)

        elif "dropbox.com" in domain:
            logger.info("Using dropbox downloader for %s", url)
            file_path = await download_dropbox(url)

        else:
            # لینک مستقیم یا ناشناخته — از downloader عمومی استفاده می‌کنیم
            logger.info("Using generic direct downloader for %s", url)
            file_path = await download_direct_link(url)

    except Exception as e:
        # لاگ خطای سرویس اختصاصی
        logger.exception("Error while using specific downloader for %s: %s", url, e)
        # ادامه می‌دهیم تا fallback انجام شود

    # اگر هنوز فایلی نگرفته‌ایم، یکبار fallback به دانلود مستقیم بزن
    if not file_path:
        try:
            logger.info("Trying fallback generic download for %s", url)
            file_path = await download_direct_link(url)
        except Exception as e:
            logger.exception("Fallback generic download failed for %s: %s", url, e)
            file_path = None

    # ارسال یا پیام خطا (فقط یکبار)
    if file_path and os.path.exists(file_path):
        try:
            await client.send_document(message.chat.id, file_path)
            logger.info("Sent file %s to chat %s", file_path, message.chat.id)
        except Exception:
            logger.exception("Failed to send file %s to chat %s", file_path, message.chat.id)
            if not gave_user_message:
                await message.reply("❌ فایل دانلود شد اما ارسالش به مشکلی برخورد کرد.")
                gave_user_message = True
        finally:
            # پاک کردن فایل محلی (هر خطا را لاگ می‌کنیم اما شکست حذف مهم نیست)
            try:
                os.remove(file_path)
            except Exception:
                logger.exception("Failed to remove temp file %s", file_path)

    else:
        # یک پیام خطای واحد به کاربر
        if not gave_user_message:
            await message.reply("❌ متأسفانه نتونستم فایل رو دانلود کنم یا فرمتش پشتیبانی نمیشه.")
