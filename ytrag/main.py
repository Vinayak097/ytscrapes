import yt_dlp
from pathlib import Path
from faster_whisper  import WhisperModel
import json 
import winsound

VIDEO_URL = "https://youtu.be/ZCNayichcKE?si=Boytn0wQedeWVxQc"

options = {
    format:"bestaudio/best"
}

model= WhisperModel(
    "large-v3",
    device="cpu",
    compute_type="int8"
)

title=""
with yt_dlp.YoutubeDL(options) as ydl:
    ydl.download(VIDEO_URL)
    videoinfo = ydl.extract_info(VIDEO_URL, download=False)
    title=videoinfo["title"]

print("video downaloded")

winsound.Beep(1000, 1000)

segments, info = model.transcribe(
    "Multi-Tenant RAG with Qdrant ｜ Free AI Engineer Course ｜ 8 Weeks [ZCNayichcKE].webm"
)


points=[]
transcript = {
    "video_id": "ZCNayichcKE",
    "title": title,
    "language": info.language,
    "segments": [
        {
            "start":segment.start,
            "text":segment.text,
            "end":segment.end
        }
        for segment in segments
    ]
}


with open("transcript.json","w",encoding="utf-8") as f:
    json.dump(transcript,f,ensure_ascii=False,indent=2)


with open("transcript.json","w",encoding="utf-8") as f:
    
    transcript = json.load(f)



CHUNK_SECONDS = 75
OVERLAP_SECONDS = 15

chunks = []

start_time = 0



winsound.Beep(1000, 1000)
print(info , segments)




