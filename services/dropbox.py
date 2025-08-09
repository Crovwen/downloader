import requests
import tempfile
import os

async def download_dropbox(url):
    if not url.endswith("?dl=1"):
        if "?dl=" in url:
            url = url.split("?dl=")[0] + "?dl=1"
        else:
            url += "?dl=1"

    temp_dir = tempfile.mkdtemp()
    local_path = os.path.join(temp_dir, url.split("/")[-1])

    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_path
    except:
        return None
