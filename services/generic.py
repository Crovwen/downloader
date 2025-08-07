import asyncio
import os
import tempfile
import requests

async def download_generic(url: str) -> str | None:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: download(url))

def download(url: str) -> str | None:
    try:
        response = requests.get(url, stream=True, timeout=15)
        content_type = response.headers.get('Content-Type', '').lower()

        # پسوند فایل رو از content-type یا URL بگیریم
        ext = guess_extension(content_type, url)
        filename = tempfile.mktemp(suffix=ext)

        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return filename if os.path.exists(filename) else None
    except Exception:
        return None

def guess_extension(content_type: str, url: str) -> str:
    import mimetypes
    ext = mimetypes.guess_extension(content_type)
    if not ext:
        # از URL بگیریم اگر نشد
        ext = os.path.splitext(url)[-1]
        if len(ext) > 5 or '/' in ext:
            return ''
    return ext or ''
