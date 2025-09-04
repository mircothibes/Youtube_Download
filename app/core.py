from yt_dlp import YoutubeDL

def download_video(url: str, path: str, audio_only: bool= False) -> None:
    options = {
        "outtmpl": f"{path}/%(title)s.%(ext)s"
    }
    if audio_only:
        options["format"] = "bestaudio/best"
        options["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    
    with YoutubeDL(options) as ydl:
        ydl.download([url])
