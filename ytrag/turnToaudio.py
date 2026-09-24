from pathlib import Path

from yt_dlp import YoutubeDL
URLS = [
    "https://www.youtube.com/watch?v=V6pRTnOZ7Mc&list=PLbJhGqY-mq47k_WLUtzVjmarUm1EuXPj2&index=10"
]


AUDIO_DIR = Path("audio")



def turn_url_to_audio():
   
    AUDIO_DIR.mkdir(exist_ok=True)
    for url in URLS:
        print("processing the url " , url)
        options = {
        "format": "bestaudio/best",
        "outtmpl": str(AUDIO_DIR / "%(id)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "m4a",
            }
        ],
    }

        with YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)
            video_id = info["id"]
            title = info["title"]
            audio_file = AUDIO_DIR / f"{video_id}.m4a"
            
            if audio_file.exists():
                print(f"Already exists: {title}")
                continue
            print("created audio file ")
            print(f"Downloading: {title}")
            
            ydl.download([url])
        
    
    











