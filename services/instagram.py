# services/instagram.py
import os
from yt_dlp import YoutubeDL

async def download_instagram(url):
    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'cookiefile': 'cookie.json'
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)
