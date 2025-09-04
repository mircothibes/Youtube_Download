import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from app.core import download_video  


def run():
    root = tk.Tk()
    root.title("YouTube Downloader")
    root.geometry("560x260")

    url_var = tk.StringVar()
    out_var = tk.StringVar()
    audio_only_var = tk.BooleanVar(value=False)

    ttk.Label(root, text="Video URL:").grid(row=0, column=0, sticky="w", padx=8, pady=6)
    url_entry = ttk.Entry(root, textvariable=url_var, width=60)
    url_entry.grid(row=0, column=1, columnspan=2, padx=8, pady=6)

    ttk.Label(root, text="Output folder:").grid(row=1, column=0, sticky="w", padx=8, pady=6)
    out_entry = ttk.Entry(root, textvariable=out_var, width=45)
    out_entry.grid(row=1, column=1, padx=8, pady=6)
    ttk.Button(root, text="Browse", command=lambda: _browse(out_var)).grid(row=1, column=2, padx=8, pady=6)

    ttk.Label(root, text="Mode:").grid(row=2, column=0, sticky="w", padx=8, pady=6)
    ttk.Radiobutton(root, text="Video", variable=audio_only_var, value=False).grid(row=2, column=1, sticky="w", padx=8)
    ttk.Radiobutton(root, text="Audio (MP3)", variable=audio_only_var, value=True).grid(row=2, column=2, sticky="w", padx=8)

    progress = ttk.Progressbar(root, mode="determinate", maximum=100)
    progress.grid(row=3, column=0, columnspan=3, sticky="ew", padx=8, pady=12)
    root.columnconfigure(1, weight=1)

    ttk.Button(root, text="Download", command=lambda: _start_download(root, url_var, out_var, audio_only_var, progress)).grid(row=4, column=1, sticky="e", padx=8, pady=8)
    ttk.Button(root, text="Close", command=root.destroy).grid(row=4, column=2, sticky="w", padx=8, pady=8)

    root.mainloop()

def _browse(out_var: tk.StringVar):
    folder = filedialog.askdirectory()
    if folder:
        out_var.set(folder)

def _start_download(root, url_var, out_var, audio_only_var, progress):
    url = url_var.get().strip()
    out_dir = out_var.get().strip()

    if not url:
        messagebox.showwarning("Validation", "Please provide a video URL.")
        return
    if not out_dir:
        messagebox.showwarning("Validation", "Please choose an output folder.")
        return

    progress["value"] = 0

    def worker():
        try:
            download_video(
                url=url,
                path=out_dir,
                audio_only=audio_only_var.get(),
                progress_cb=lambda d: _on_progress_safe(root, progress, d),
            )
        except Exception as e:
            msg = str(e)
            root.after(0, lambda m=msg: messagebox.showerror("Error", m))
        else:
            root.after(0, lambda: messagebox.showinfo("Done", "Download completed!"))

    threading.Thread(target=worker, daemon=True).start()

def _on_progress_safe(root, progress, data: dict):
    """
    data: dict do hook do yt-dlp (status, downloaded_bytes, total_bytes, etc.)
    """
    status = data.get("status")
    if status == "downloading":
        downloaded = data.get("downloaded_bytes") or 0
        total = data.get("total_bytes") or data.get("total_bytes_estimate") or 0
        if total:
            pct = (downloaded / total) * 100
            root.after(0, lambda: progress.configure(value=pct))
    elif status == "finished":
        root.after(0, lambda: progress.configure(value=100))
