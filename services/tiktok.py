import tempfile
import yt_dlp
import asyncio
import os

async def download_tiktok(url):
    temp_dir = tempfile.mkdtemp()
    output_path = os.path.join(temp_dir, "%(title)s.%(ext)s")

    ydl_opts = {
        "outtmpl": output_path,
        "format": "best"
    }

    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).download([url]))

        for file in os.listdir(temp_dir):
            return os.path.join(temp_dir, file)
    except:
        return None
