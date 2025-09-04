from typing import Callable, Optional
from yt_dlp import YoutubeDL

def download_video(url: str, path: str, audio_only: bool = False, progress_cb: Optional[Callable[[dict], None]] = None) -> None:
    def _hook(d: dict):
        if progress_cb:
            progress_cb(d)

    options =options = {
    "outtmpl": f"{path}/%(title)s.%(ext)s",
    "format": "bv*+ba/b",            
    "merge_output_format": "mp4",    
}
    if audio_only:
        options["format"] = "bestaudio/best"
        options["postprocessors"] = [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}
        ]
    else:
        options["format"] = "bv*+ba/b"

    with YoutubeDL(options) as ydl:
        ydl.download([url])
