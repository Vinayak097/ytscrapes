from pathlib import Path
import yt_dlp
from faster_whisper import WhisperModel


VIDEO_URL = "https://youtu.be/ZCNayichcKE?si=_AO_ON5U_yJsRpXF"

AUDIO_DIR = Path("audio")
TRANSCRIPT_DIR = Path("transcripts")

AUDIO_DIR.mkdir(exist_ok=True)
TRANSCRIPT_DIR.mkdir(exist_ok=True)


# -------------------------
# STEP 1: Download audio
# -------------------------

print("Downloading audio...")

ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": str(AUDIO_DIR / "%(id)s.%(ext)s"),
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
            "preferredquality": "192",
        }
    ],
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(VIDEO_URL, download=True)

video_id = info["id"]
title = info["title"]

audio_path = AUDIO_DIR / f"{video_id}.wav"

print(f"Video: {title}")
print(f"Audio: {audio_path}")


# -------------------------
# STEP 2: Transcribe
# -------------------------

print("Loading Whisper model...")

model = WhisperModel(
    "large-v3",
    device="cpu",
    compute_type="int8",
)

print("Transcribing...")

segments, info = model.transcribe(
    str(audio_path),
    language="en",
    condition_on_previous_text=False,
)

transcript = []

for segment in segments:
    item = {
        "start": segment.start,
        "end": segment.end,
        "text": segment.text.strip(),
    }

    transcript.append(item)

    print(
        f"[{segment.start:.2f} - {segment.end:.2f}] "
        f"{segment.text.strip()}"
    )


# -------------------------
# STEP 3: Save transcript
# -------------------------

output_path = TRANSCRIPT_DIR / f"{video_id}.json"

import json

data = {
    "video_id": video_id,
    "title": title,
    "language": info.language,
    "segments": transcript,
}

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print()
print("Done!")
print(f"Transcript saved to: {output_path}")