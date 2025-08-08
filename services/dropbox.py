import requests

def download_dropbox(url: str, save_path: str):
    """
    دانلود مستقیم از Dropbox.
    اگه لینک preview باشه، تبدیل به لینک direct می‌کنیم.
    """
    try:
        # اگه لینک preview باشه، تبدیلش می‌کنیم به direct
        if "www.dropbox.com" in url and not url.endswith("?dl=1"):
            if "?dl=0" in url:
                url = url.replace("?dl=0", "?dl=1")
            else:
                url += "?dl=1"

        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return f"Downloaded successfully to {save_path}"
    except Exception as e:
        return f"Error downloading from Dropbox: {e}" 
