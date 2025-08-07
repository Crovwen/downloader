import yt_dlp
import asyncio
import os
import tempfile

async def download_youtube(url: str) -> str | None:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, sync_download, url)

def sync_download(url: str) -> str | None:
    temp_dir = tempfile.mkdtemp()
    ydl_opts = {
        'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
        'format': 'best[ext=mp4]/best',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            if not info:
                return None
            if 'entries' in info:
                info = info['entries'][0]  # اولین ویدیو اگر پلی لیست باشه
            filename = ydl.prepare_filename(info)
            return filename if os.path.exists(filename) else None
        except Exception:
            return None
