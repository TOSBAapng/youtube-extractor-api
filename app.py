```python
from flask import Flask, request, jsonify
import yt_dlp
import os
import subprocess

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "success": True,
        "message": "YouTube Extractor API çalışıyor."
    })


@app.route("/debug", methods=["GET"])
def debug():
    try:
        version_result = subprocess.run(
            ["yt-dlp", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )

        deno_result = subprocess.run(
            ["deno", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )

        return jsonify({
            "success": True,
            "yt_dlp_version": version_result.stdout.strip(),
            "yt_dlp_error": version_result.stderr.strip(),
            "deno": deno_result.stdout.strip(),
            "deno_error": deno_result.stderr.strip(),
            "message": "Temel sistem testleri başarılı. YouTube extraction testi /extract üzerinden yapılacak."
        })

    except subprocess.TimeoutExpired:
        return jsonify({
            "success": False,
            "error": "Sistem testi zaman aşımına uğradı."
        }), 500

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/extract", methods=["POST"])
def extract():
    try:
        data = request.get_json(silent=True) or {}
        youtube_url = data.get("url")

        if not youtube_url:
            return jsonify({
                "success": False,
                "error": "URL gerekli."
            }), 400

        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,

            "format": "best[ext=mp4]/best",

            "skip_download": True,

            "socket_timeout": 30,

            "retries": 1,

            "extractor_args": {
                "youtubepot-bgutilhttp": {
                    "base_url": "http://127.0.0.1:4416"
                }
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                youtube_url,
                download=False
            )

        return jsonify({
            "success": True,
            "title": info.get("title"),
            "duration": info.get("duration"),
            "thumbnail": info.get("thumbnail"),
            "url": info.get("url"),
            "webpage_url": info.get("webpage_url")
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))

    app.run(
        host="0.0.0.0",
        port=port
    )
```
