import json
import os
import winsound
from pathlib import Path

import yt_dlp
from faster_whisper import WhisperModel

# Put all cache/model downloads on D: to avoid C: drive issues.
D_DRIVE_ROOT = Path(r"D:\ytscrapes")
D_DRIVE_ROOT.mkdir(parents=True, exist_ok=True)

os.environ.setdefault("HF_HOME", str(D_DRIVE_ROOT / "hf_cache"))
os.environ.setdefault("HUGGINGFACE_HUB_CACHE", str(D_DRIVE_ROOT / "hf_cache" / "hub"))
os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS", "1")
os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")

VIDEO_URL = "https://youtu.be/ZCNayichcKE?si=Boytn0wQedeWVxQc"
AUDIO_DIR = D_DRIVE_ROOT / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_JSON = D_DRIVE_ROOT / "transcript.json"

# Use a smaller model to avoid the huge 3GB "large-v3" download and Windows symlink issues.
MODEL_NAME = "tiny"


def download_audio(video_url: str) -> tuple[str, str]:
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(AUDIO_DIR / "%(id)s.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)

    video_id = info["id"]
    title = info["title"]
    audio_path = str(AUDIO_DIR / f"{video_id}.webm")
    return title, audio_path


def main() -> None:
    print("Downloading audio...")
    title, audio_path = download_audio(VIDEO_URL)
    print(f"Downloaded: {audio_path}")

    print("Loading Whisper model...")
    model = WhisperModel(MODEL_NAME, device="cpu", compute_type="int8")

    print("Transcribing...")
    segments, info = model.transcribe(audio_path, language="en")

    transcript = {
        "video_id": "ZCNayichcKE",
        "title": title,
        "language": info.language,
        "segments": [
            {
                "start": segment.start,
                "end": segment.end,
                "text": segment.text,
            }
            for segment in segments
        ],
    }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(transcript, f, ensure_ascii=False, indent=2)

    print(f"Transcript saved to: {OUTPUT_JSON}")
    winsound.Beep(1000, 1000)


if __name__ == "__main__":
    main()




