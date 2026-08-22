# ytUi.py
# Created by Jarred on 2026-07-22
# Powered by yt-dlp
# To install yt-dlp, run: pip install yt-dlp

import subprocess
import threading
import tkinter as tk
from tkinter import font
from tkinter.scrolledtext import ScrolledText
import tkinter.messagebox as messagebox
import tkinter.filedialog
import webbrowser as browser
import os
import sys
import yt_dlp
import shutil

isPicked = False
downloadPath = ""

class TextLogger:
    def debug(self, msg):
        append_log(msg)

    def warning(self, msg):
        append_log("WARNING: " + msg)

    def error(self, msg):
        append_log("ERROR: " + msg)


def append_log(text):
    logBar.config(state="normal")
    logBar.insert(tk.END, text + "\n")
    logBar.see(tk.END)
    logBar.config(state="disabled")
    
    
def clear_log_clicked():
    if messagebox.askyesno("Clear?", "Are you sure to clear all logs?", parent=root):
        logBar.config(state="normal")
        logBar.delete("1.0", tk.END)
        logBar.config(state="disabled")

def download_youtube_video(url, playlist):
    ydl_opts = {
        # Downloads a single file with video+audio (no FFmpeg required)
        "format": 
        "bv*[height=720]+ba/b[height=720]" if not audio_var.get() else "bestaudio/best",
        'allow_playlist_files': True,
        "noplaylist": not playlist,
        "logger": TextLogger(),       
        "verbose": False,
        "quiet": False,       
        "no_warnings": False,
        "progress_hooks": [lambda d: append_log(f"Progress: {d['status']} - {d.get('downloaded_bytes', 0)} bytes downloaded")],
        "outtmpl": os.path.join(downloadPath, "%(title)s.%(ext)s") if isPicked else "%(title)s.%(ext)s"
    }

    try:
        append_log("Starting download...")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        append_log("Download completed!")

    except Exception as e:
        append_log("ERROR: " + str(e))


def download_button_clicked():
    url = urlBox.get().strip()

    if not url:
        append_log("Please enter a YouTube URL.")
        return

    threading.Thread(
        target=download_youtube_video,
        args=(url, playlist_var.get()),
        daemon=True
    ).start()

    append_log("Download completed!")

    if isPicked:
        append_log(f"The path you downloaded is at: {downloadPath}")
        #subprocess.Popen(f'explorer "{downloadPath}"')
    else:
        append_log("No download path selected. Downloaded files will be saved in the current working directory.")

def show_youtube_website_tkwindow():
    messagebox.showinfo("Open YouTube Website", 
                        "You will be redirected to the YouTube website. " \
                        "To download videos, please copy the URL from your browser and paste it into the input field in this application.", 
                        parent=root,
                        icon='info')

    if messagebox.askyesno("Open YouTube Website", "Do you want to open the YouTube website in your default browser?", parent=root):
        browser.open("https://www.youtube.com")

def select_download_path():
    global isPicked, downloadPath

    downloadPath = tkinter.filedialog.askdirectory(
        title="Select Download Path",
        parent=root
    )

    if downloadPath:
        isPicked = True
        append_log(f"Download path set to: {downloadPath}")
    else:
        isPicked = False
        downloadPath = ""
        append_log("No download path selected.")
        
def resource_path(filename):
    if getattr(sys, "frozen", False):
        return os.path.join(os.path.dirname(sys.executable), filename)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)


# ---------------- GUI ----------------

ico = resource_path("1000088823.ico")

root = tk.Tk()
root.title("YtBro - A YouTube Downloader by Jarred")
root.geometry("700x450")

try:
    root.iconbitmap(ico)
except tk.TclError:
    messagebox.showinfo("Error", "YtBro cannot find the icon file. It maybe renamed or deleted...", parent=root)
    

root.configure(bg="#DDA756")

tk.Label(root, text="YtBro", font=font.Font(weight="bold", size=24), bg="#bf1408", foreground="white", anchor="center").pack(fill="both", expand=True)
tk.Label(root, text="YouTube Downloader by Jarred (Powered by yt-dlp)", font=font.Font(weight="bold", size=12), bg="#bf1408", foreground="white", anchor="center").pack(fill="both", expand=True, pady=(0, 5))


tk.Label(root, text="Enter YouTube URL:", font=font.Font(weight="bold", size=12), anchor="w", bg="#DDA756").pack(fill="x", expand=True, pady=2, padx=10, anchor="w")

urlBox = tk.Entry(root, bg="#faaaaa", font=font.Font(size=12))
urlBox.pack(fill="x", expand=True, padx=10, pady=5)

ytWebButton = tk.Button(root, text="Open YouTube Website", command=show_youtube_website_tkwindow, bg="#bf1408", fg="white")
ytWebButton.pack(pady=5, padx=10, anchor="nw")

playlist_var = tk.BooleanVar(value=False)
audio_var = tk.BooleanVar(value=False)

tk.Label(root, text="Settings:", font=font.Font(weight="bold", size=12), anchor="w", bg="#DDA756").pack(fill="x", expand=True, pady=2, padx=10, anchor="w")

playlist_check = tk.Checkbutton(
    root,
    text="Download Playlist",
    variable=playlist_var,
    bg="#DDA756",
)
playlist_check.pack(padx=10, pady=5, anchor="nw")

audio_check = tk.Checkbutton(
    root,
    text="Download Audio Only",
    variable=audio_var,
    bg="#DDA756",
)
audio_check.pack(padx=10, pady=5, anchor="nw")

pathPicker = tk.Button(
    root,
    text="Select Download Path",
    command=select_download_path,
    bg="#bf1408",
    fg="white"
)
pathPicker.pack(fill="x", expand=True, pady=(0, 10))

clearLogBtn = tk.Button(
    root,
    text="Clear Log Text",
    command=clear_log_clicked,
    bg="#bf1408",
    fg="white",
)
clearLogBtn.pack(fill="x", expand=True, pady=(0, 10))

downloadBtn = tk.Button(
    root,
    text="Download",
    command=download_button_clicked,
    bg="#bf1408",
    fg="white",
)
downloadBtn.pack(fill="x", expand=True, pady=(0, 10))

logBar = ScrolledText(
    root,
    width=80,
    height=18,
    state="disabled",
    wrap=tk.WORD,
    bg="#faaaaa"
)
logBar.pack(fill="both", expand=True, padx=10, pady=10)

root.mainloop()

