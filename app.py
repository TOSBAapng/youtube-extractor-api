from flask import Flask, request, jsonify
import yt_dlp
import os
import subprocess
import urllib.request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "success": True,
        "message": "YouTube Extractor API çalışıyor."
    })


@app.route("/debug", methods=["GET"])
def debug():
    result = {
        "success": True
    }

    try:
        yt = subprocess.run(
            ["yt-dlp", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )

        result["yt_dlp_version"] = yt.stdout.strip()
        result["yt_dlp_error"] = yt.stderr.strip()

    except Exception as e:
        result["yt_dlp_error"] = str(e)

    try:
        deno = subprocess.run(
            ["deno", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )

        result["deno"] = deno.stdout.strip()
        result["deno_error"] = deno.stderr.strip()

    except Exception as e:
        result["deno_error"] = str(e)

    try:
        response = urllib.request.urlopen(
            "http://127.0.0.1:4416/ping",
            timeout=5
        )

        result["bgutil"] = {
            "running": True,
            "status": response.status
        }

    except Exception as e:
        result["bgutil"] = {
            "running": False,
            "error": str(e)
        }

    return jsonify(result)


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

            "quiet": False,

            "no_warnings": False,

            "noplaylist": True,

            "format": "best[ext=mp4]/best",

            "skip_download": True,

            "socket_timeout": 30,

            "retries": 1,

            "extractor_args": {

                "youtube": {

                    "player_client": [
                        "mweb"
                    ]

                },

                "youtubepot-bgutilhttp": {

                    "base_url":
                        "http://127.0.0.1:4416"

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

            "webpage_url":
                info.get("webpage_url")

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            8080
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
