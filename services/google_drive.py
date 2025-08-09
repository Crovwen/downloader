import requests
import tempfile
import os

async def download_google_drive(url):
    file_id = None
    if "id=" in url:
        file_id = url.split("id=")[-1]
    elif "/d/" in url:
        file_id = url.split("/d/")[1].split("/")[0]

    if not file_id:
        return None

    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

    temp_dir = tempfile.mkdtemp()
    local_path = os.path.join(temp_dir, f"{file_id}.file")

    try:
        with requests.get(download_url, stream=True) as r:
            r.raise_for_status()
            with open(local_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_path
    except:
        return None
