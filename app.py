from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "success": True,
        "message": "YouTube Extractor API çalışıyor."
    })


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
            "skip_download": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)

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
    app.run(host="0.0.0.0", port=port)
