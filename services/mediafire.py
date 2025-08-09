import requests
import tempfile
import os
import re

async def download_mediafire(url):
    try:
        page = requests.get(url).text
        dl_url = re.search(r'href="(https://download[^"]+)"', page).group(1)

        temp_dir = tempfile.mkdtemp()
        local_path = os.path.join(temp_dir, dl_url.split("/")[-1])

        with requests.get(dl_url, stream=True) as r:
            r.raise_for_status()
            with open(local_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        return local_path
    except:
        return None
