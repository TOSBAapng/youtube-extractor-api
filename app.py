from flask import Flask, request, jsonify
import yt_dlp
import os
import subprocess

app = Flask(**name**)

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
text=True
)


    deno_result = subprocess.run(
        ["deno", "--version"],
        capture_output=True,
        text=True
    )

    ejs_result = subprocess.run(
        [
            "yt-dlp",
            "--verbose",
            "--simulate",
            "https://www.youtube.com/watch?v=2SKZLVD8NyE"
        ],
        capture_output=True,
        text=True,
        timeout=60
    )

    return jsonify({
        "success": True,
        "yt_dlp_version": version_result.stdout.strip(),
        "yt_dlp_error": version_result.stderr.strip(),
        "deno": deno_result.stdout.strip(),
        "deno_error": deno_result.stderr.strip(),
        "yt_dlp_debug": ejs_result.stdout[-12000:],
        "yt_dlp_debug_error": ejs_result.stderr[-12000:]
    })

except subprocess.TimeoutExpired:
    return jsonify({
        "success": False,
        "error": "yt-dlp debug işlemi 60 saniye içinde tamamlanmadı."
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
        "skip_download": True
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


if **name** == "**main**":
port = int(os.environ.get("PORT", 8080))
app.run(
host="0.0.0.0",
port=port
)
