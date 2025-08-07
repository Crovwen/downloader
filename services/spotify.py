import yt_dlp
import asyncio
import os
import tempfile

async def download_spotify(url: str) -> str | None:
    # فقط عنوان رو از اسپاتیفای بگیر و سرچ کن تو یوتیوب
    query = await extract_title_from_spotify_url(url)
    if not query:
        return None
    return await download_from_youtube_search(query)

async def extract_title_from_spotify_url(url: str) -> str | None:
    # فقط برای نمایش ایده، واقعی پیاده‌سازی نیازمند API اسپاتیفای هست
    # در این نسخه ساده فقط لینک رو پاس می‌دیم به yt-dlp برای دریافت اطلاعات
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: get_title(url))

def get_title(url: str) -> str | None:
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            return info.get('title')
    except Exception:
        return None

async def download_from_youtube_search(query: str) -> str | None:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: download(query))

def download(query: str) -> str | None:
    temp_dir = tempfile.mkdtemp()
    ydl_opts = {
        'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'format': 'bestaudio/best',
        'default_search': 'ytsearch',
        'noplaylist': True
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            if 'entries' in info:
                info = info['entries'][0]
            filename = ydl.prepare_filename(info)
            return filename if os.path.exists(filename) else None
    except Exception:
        return None
