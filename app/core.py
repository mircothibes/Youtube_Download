# app/core.py
from typing import Callable, Optional
from yt_dlp import YoutubeDL
import shutil, os

def _get_ffmpeg_dir() -> Optional[str]:
    """
    Returns the directory that contains ffmpeg.exe (if found on PATH),
    or None otherwise.
    """
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        return os.path.dirname(ffmpeg_path)
    return None

def download_video(
    url: str,
    path: str,
    audio_only: bool = False,
    progress_cb: Optional[Callable[[dict], None]] = None,
    ffmpeg_dir: Optional[str] = None,  # allow manual override
) -> None:
    def _hook(d: dict):
        if progress_cb:
            progress_cb(d)

    # Try to auto-detect ffmpeg if not provided
    ffmpeg_dir = ffmpeg_dir or _get_ffmpeg_dir()

    ydl_opts: dict = {
        "outtmpl": f"{path}/%(title)s.%(ext)s",
        "progress_hooks": [_hook],
        "color": "never",  # avoid ANSI codes in error messages
    }

    if ffmpeg_dir:                 # <- key point
        ydl_opts["ffmpeg_location"] = ffmpeg_dir

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
        ydl_opts.update({
            "format": "bv*+ba/b",         # best video + best audio; fallback to best
            "merge_output_format": "mp4", # needs ffmpeg
        })

    # If ffmpeg is required and still not found, raise a clear error
    if not ffmpeg_dir and not audio_only:
        raise RuntimeError(
            "FFmpeg not found. Please install FFmpeg or pass ffmpeg_dir to download_video()."
        )

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
