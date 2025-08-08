#!/usr/bin/env python3
# main.py
import os
import sys
import time
import threading
import subprocess
from flask import Flask, jsonify

ROOT = os.path.dirname(__file__)
BOT_SCRIPT = os.path.join(ROOT, "bot_runner.py")

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Auto-downloader bot service is alive!", 200

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

def start_and_watch_bot():
    """
    این تابع یک لوپ نامحدود اجرا می‌کنه که:
    - bot_runner.py رو با همان پایتون فعلی اجرا می‌کنه
    - خروجی stdout/stderr بات رو خوانده و چاپ می‌کنه (قابل دیدن در لاگ Render)
    - اگر بات کرش کرد، بعد از 5 ثانیه مجدداً ریستارت می‌کنه
    """
    python = sys.executable  # اطمینان از استفاده از همان مفسر و virtualenv
    env = os.environ.copy()
    while True:
        try:
            proc = subprocess.Popen(
                [python, BOT_SCRIPT],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                env=env
            )
            print(f"[SUPERVISOR] bot process started (pid={proc.pid})")
            # stream کردن لاگ بات به لاگ اصلی
            if proc.stdout:
                for raw in iter(proc.stdout.readline, b''):
                    if not raw:
                        break
                    try:
                        line = raw.decode(errors='replace').rstrip()
                    except:
                        line = str(raw)
                    print(f"[BOT] {line}")
            ret = proc.wait()
            print(f"[SUPERVISOR] bot exited with code {ret}. Restarting in 5s...")
        except Exception as e:
            print(f"[SUPERVISOR] exception while starting bot: {e}")
        time.sleep(5)

if __name__ == "__main__":
    # run supervisor thread (daemon so it won't block shutdown)
    t = threading.Thread(target=start_and_watch_bot, daemon=True)
    t.start()

    # Run Flask (Render expects a web port)
    port = int(os.environ.get("PORT", 10000))
    # Optional: set host to 0.0.0.0 to be reachable
    app.run(host="0.0.0.0", port=port)
    
