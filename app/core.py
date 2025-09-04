from typing import Callable, Optional
from yt_dlp import YoutubeDL

def download_video(url: str, path: str, audio_only: bool = False, progress_cb: Optional[Callable[[dict], None]] = None) -> None:
    def _hook(d: dict):
        if progress_cb:
            progress_cb(d)

    ydl_opts = {
        "outtmpl": f"{path}/%(title)s.%(ext)s",
        "progress_hooks": [_hook],
    }

    if audio_only:
        ydl_opts.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        })
    else:
        # Melhor vídeo + áudio, cai para melhor único se necessário
        ydl_opts.update({
            "format": "bv*+ba/b",
            "merge_output_format": "mp4",
        })

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
