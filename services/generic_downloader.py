import requests
import tempfile
import os
import asyncio

async def download_direct_link(url):
    try:
        temp_dir = tempfile.mkdtemp()
        local_filename = os.path.join(temp_dir, url.split("/")[-1])

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: _download(url, local_filename))

        return local_filename if os.path.exists(local_filename) else None
    except:
        return None

def _download(url, path):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
