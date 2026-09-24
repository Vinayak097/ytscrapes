import json
from pathlib import Path
from faster_whisper import WhisperModel

AUDIO_DIR = Path("audio")
TRANSCRIPT_FILE = Path("transcripts.json")

def generate_transcript():

    if TRANSCRIPT_FILE.exists():
        with open(TRANSCRIPT_FILE, "r", encoding="utf-8") as file:
            transcripts = json.load(file)
    else:
        transcripts = []

    processed_ids = {
        transcript["video_id"]
        for transcript in transcripts
    }

    model = WhisperModel(
        "small",
        device="cpu",
        compute_type="int8"
    )

    for audio_file in AUDIO_DIR.iterdir():

        if not audio_file.is_file():
            continue

        video_id = audio_file.stem

        # Already exists in transcripts.json
        if video_id in processed_ids:
            print(f"Already processed: {audio_file.name}")
            continue

        print(f"Transcribing: {audio_file.name}")

        segments, info = model.transcribe(
            str(audio_file),
            vad_filter=True
        )

        transcript_segments = []

        for segment in segments:
            transcript_segments.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip()
            })

        transcript_object = {
            "video_id": video_id,
            "audio_file": audio_file.name,
            "language": info.language,
            "segments": transcript_segments
        }

        transcripts.append(transcript_object)

        with open(TRANSCRIPT_FILE, "w", encoding="utf-8") as file:
            json.dump(
                transcripts,
                file,
                indent=2,
                ensure_ascii=False
            )

        processed_ids.add(video_id)

        print(f"Saved: {audio_file.name}")


__all__ = ["generate_transcript"]