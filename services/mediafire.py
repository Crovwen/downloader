import requests

def download_mediafire(url: str, save_path: str):
    # فرض بر این است که URL به یک فایل مستقیم اشاره می‌کنه.
    try:
        response = requests.get(url)
        with open(save_path, 'wb') as file:
            file.write(response.content)
        return f"Download successful! File saved to {save_path}"
    except Exception as e:
        return f"Error occurred: {e}"
