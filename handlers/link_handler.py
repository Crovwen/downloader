import os
import tempfile
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

async def handle_link(client, message, url):
    domain = urlparse(url).netloc.lower()
    file_path = None

    if "t.me" in domain or "telegram" in domain:
        await message.reply("❌ پشتیبانی از لینک‌های تلگرام انجام نمی‌شود.")
        return

    try:
        if any(x in domain for x in ["youtube.com", "youtu.be"]):
            file_path = await download_youtube(url)
        elif "instagram.com" in domain:
            file_path = await download_instagram(url)
        elif "tiktok.com" in domain:
            file_path = await download_tiktok(url)
        elif "pinterest.com" in domain:
            file_path = await download_pinterest(url)
        elif "soundcloud.com" in domain:
            file_path = await download_soundcloud(url)
        elif "spotify.com" in domain:
            file_path = await download_spotify(url)
        elif any(x in domain for x in ["drive.google.com", "docs.google.com"]):
            file_path = await download_google_drive(url)
        elif "mediafire.com" in domain:
            file_path = await download_mediafire(url)
        elif "dropbox.com" in domain:
            file_path = await download_dropbox(url)
        else:
            file_path = await download_direct_link(url)

        if file_path and os.path.exists(file_path):
            await client.send_document(message.chat.id, file_path)
            os.remove(file_path)
        else:
            await message.reply("❌ متأسفانه نتونستم فایل رو دانلود کنم یا فرمتش پشتیبانی نمیشه.")

    except Exception as e:
        await message.reply(f"⚠️ خطا: {str(e)}")
        
