import requests

def download_direct_link(url: str, save_path: str):
    """
    دانلود هر لینکی که مستقیم به فایل اشاره می‌کند.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return f"Downloaded successfully to {save_path}"
    except Exception as e:
        return f"Error downloading from direct link: {e}"
      
