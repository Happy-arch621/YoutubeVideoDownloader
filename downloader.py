import yt_dlp
from tkinter import filedialog
import os
import sys



def get_base_path():
    # Cuando corre como .exe (PyInstaller)
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    # Cuando corre como script normal
    return os.path.dirname(os.path.abspath(__file__))



def get_video_info(url):
    with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
        info = ydl.extract_info(url, download=False)

    return {
        "title": info.get("title"),
        "duration": info.get("duration"),
        "thumbnail": info.get("thumbnail"),
    }



def progress_hook(d, progress_callback=None):
    if d["status"] == "downloading":
        percent = d.get("_percent_str", "").strip()
        speed = d.get("_speed_str", "")
        eta = d.get("_eta_str", "")

        if progress_callback:
            progress_callback(percent, speed, eta)

    elif d["status"] == "finished":
        if progress_callback:
            progress_callback("100%", "", "Finalizando...")



def download_video(url, progress_callback=None):

    info = get_video_info(url)
    title = info["title"]

    file_path = filedialog.asksaveasfilename(
        initialfile=f"{title}.mp4",
        defaultextension=".mp4",
        filetypes=[("Video MP4", "*.mp4")],
        title="Guardar video como..."
    )

    if not file_path:
        return False


    base_path = get_base_path()

    ydl_opts = {
        "outtmpl": file_path,
        "format": "bv*+ba/b",
        "merge_output_format": "mp4",
        "ffmpeg_location": base_path,
        "progress_hooks": [
            lambda d: progress_hook(d, progress_callback)
        ],
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return True