"""
Song Identifier Web App
Plak 'n video-skakel (Facebook, TikTok, YouTube, ens.) en kry die liedjie se naam.
"""

import os
import subprocess
import tempfile
import requests
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

AUDD_API_KEY = os.environ.get("AUDD_API_KEY", "")
AUDD_URL = "https://api.audd.io/"


def download_and_trim_audio(video_url: str, tmp_dir: str) -> str:
    raw_path = os.path.join(tmp_dir, "audio.%(ext)s")
    downloaded_mp3 = os.path.join(tmp_dir, "audio.mp3")
    trimmed_path = os.path.join(tmp_dir, "trimmed.mp3")

    dl_cmd = ["yt-dlp", "-x", "--audio-format", "mp3", "-o", raw_path, video_url]
    result = subprocess.run(dl_cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        raise RuntimeError(f"Kon nie video aflaai nie: {result.stderr[-500:]}")

    trim_cmd = [
        "ffmpeg", "-y", "-i", downloaded_mp3,
        "-t", "20", "-ac", "1", "-ar", "44100", trimmed_path,
    ]
    subprocess.run(trim_cmd, check=True, capture_output=True, timeout=60)
    return trimmed_path


def identify_song(audio_path: str) -> dict:
    with open(audio_path, "rb") as f:
        files = {"file": f}
        data = {"api_token": AUDD_API_KEY, "return": "spotify,apple_music"}
        response = requests.post(AUDD_URL, data=data, files=files, timeout=30)
    response.raise_for_status()
    return response.json()


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/identify", methods=["POST"])
def identify():
    video_url = request.form.get("video_url", "").strip()
    if not video_url:
        return jsonify({"error": "Geen skakel ontvang nie."}), 400
    if not AUDD_API_KEY:
        return jsonify({"error": "AUDD_API_KEY is nie opgestel op die bediener nie."}), 500

    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            trimmed_path = download_and_trim_audio(video_url, tmp_dir)
            result = identify_song(trimmed_path)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if result.get("status") == "success" and result.get("result"):
        song = result["result"]
        return jsonify({
            "found": True,
            "title": song.get("title"),
            "artist": song.get("artist"),
            "album": song.get("album"),
            "spotify": (song.get("spotify") or {}).get("external_urls", {}).get("spotify"),
        })
    return jsonify({"found": False})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
