import asyncio
import os
import tempfile
import requests

async def download_gdrive(url: str) -> str | None:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: download(url))

def download(url: str) -> str | None:
    try:
        file_id = extract_file_id(url)
        if not file_id:
            return None
        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        response = requests.get(download_url, stream=True)
        if 'text/html' in response.headers.get('content-type', ''):
            return None
        filename = tempfile.mktemp()
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        return filename
    except Exception:
        return None

def extract_file_id(url: str) -> str | None:
    import re
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    match = re.search(r'id=([a-zA-Z0-9_-]+)', url)
    return match.group(1) if match else None
