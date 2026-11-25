# ytBro.py
# Created by Jarred on 2026-07-22
# Powered by yt-dlp
# To install yt-dlp, run: pip install yt-dlp

import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import tkinter.messagebox as messagebox
import tkinter.filedialog

import webbrowser as browser

import os
import sys
import yt_dlp
import threading

isPicked = False
downloadPath = ""

base_dir = os.path.dirname(os.path.abspath(__file__))
ffmpeg_path = os.path.join(base_dir, "ffmpeg-master-latest-win64-gpl", "bin", "ffmpeg.exe")

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
        "ffmpeg_location": ffmpeg_path,
        "format": 
        "bv*[height=720]+ba/b[height=720]" if not audio_var.get() else "bestaudio/best",
        'allow_playlist_files': True,
        "noplaylist": not playlist,
        "logger": TextLogger(),       
        "verbose": False,
        "quiet": False,       
        "no_warnings": False,
        "merge_output_format": "mp4" if not audio_var.get() else "m4a",
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
        path_var.set(downloadPath)
        append_log(f"Download path set to: {downloadPath}")
    else:
        isPicked = False
        downloadPath = ""
        path_var.set("Downloads will be saved in the current folder")
        append_log("No download path selected.")
        
def resource_path(filename):
    if getattr(sys, "frozen", False):
        return os.path.join(os.path.dirname(sys.executable), filename)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)


# ---------------- GUI ----------------

ico = resource_path("1000088823.ico")

root = tk.Tk()
root.title("YtBro - A YouTube Downloader by Jarred")
root.geometry("860x620")
root.minsize(760, 560)

try:
    root.iconbitmap(ico)
except tk.TclError:
    messagebox.showinfo("Error", "YtBro cannot find the icon file. It maybe renamed or deleted...", parent=root)

colors = {
    "background": "#12090b",
    "panel": "#211114",
    "field": "#180b0e",
    "text": "#fff1f2",
    "muted": "#c4a3a8",
    "accent": "#e11d48",
    "accent_hover": "#be123c",
    "border": "#48212a",
}

root.configure(bg=colors["background"])
style = ttk.Style(root)
if "clam" in style.theme_names():
    style.theme_use("clam")

style.configure("App.TFrame", background=colors["background"])
style.configure("Card.TFrame", background=colors["panel"])
style.configure(
    "Body.TLabel",
    background=colors["panel"],
    foreground=colors["text"],
    font=("Segoe UI", 10),
)
style.configure(
    "Muted.TLabel",
    background=colors["panel"],
    foreground=colors["muted"],
    font=("Segoe UI", 9),
)
style.configure(
    "Section.TLabel",
    background=colors["panel"],
    foreground=colors["text"],
    font=("Segoe UI", 12, "bold"),
)
style.configure(
    "Modern.TEntry",
    fieldbackground=colors["field"],
    foreground=colors["text"],
    padding=10,
    borderwidth=0,
)
style.configure(
    "Card.TCheckbutton",
    background=colors["panel"],
    foreground=colors["text"],
    font=("Segoe UI", 10),
    padding=4,
)
style.map(
    "Card.TCheckbutton",
    background=[("active", colors["panel"])],
    foreground=[("active", colors["accent"])],
)
style.configure(
    "Modern.TButton",
    background=colors["border"],
    foreground=colors["text"],
    font=("Segoe UI", 10, "bold"),
    padding=(12, 9),
    borderwidth=0,
)
style.map(
    "Modern.TButton",
    background=[("active", "#5d2934"), ("pressed", "#371820")],
)
style.configure(
    "Download.TButton",
    background=colors["accent"],
    foreground="#ffffff",
    font=("Segoe UI", 11, "bold"),
    padding=(14, 11),
    borderwidth=0,
)
style.map(
    "Download.TButton",
    background=[("active", colors["accent_hover"]), ("pressed", "#9f1239")],
)

header = tk.Frame(root, bg="#1b0c10", padx=24, pady=18)
header.pack(fill="x")
tk.Label(
    header,
    text="YtBro",
    bg="#1b0c10",
    fg=colors["text"],
    font=("Segoe UI", 25, "bold"),
).pack(anchor="w")
tk.Label(
    header,
    text="A YouTube Downloader by Jarred",
    bg="#1b0c10",
    fg=colors["muted"],
    font=("Segoe UI", 10),
).pack(anchor="w", pady=(2, 0))

content = ttk.Frame(root, style="App.TFrame", padding=18)
content.pack(fill="both", expand=True)
content.columnconfigure(0, weight=4, minsize=290)
content.columnconfigure(1, weight=5, minsize=350)
content.rowconfigure(0, weight=1)

controls = ttk.Frame(content, style="App.TFrame")
controls.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
controls.columnconfigure(0, weight=1)
controls.rowconfigure(1, weight=1)

url_card = ttk.Frame(controls, style="Card.TFrame", padding=16)
url_card.grid(row=0, column=0, sticky="new", pady=(0, 12))
url_card.columnconfigure(0, weight=1)
ttk.Label(url_card, text="Video URL", style="Section.TLabel").grid(
    row=0, column=0, sticky="w"
)
ttk.Label(
    url_card,
    text="Paste a YouTube video or playlist link",
    style="Muted.TLabel",
).grid(row=1, column=0, sticky="w", pady=(3, 10))
urlBox = ttk.Entry(url_card, font=("Segoe UI", 11), style="Modern.TEntry")
urlBox.grid(row=2, column=0, sticky="ew", pady=(0, 10))
ytWebButton = ttk.Button(
    url_card,
    text="Open YouTube",
    command=show_youtube_website_tkwindow,
    style="Modern.TButton",
)
ytWebButton.grid(row=3, column=0, sticky="ew")

playlist_var = tk.BooleanVar(value=False)
audio_var = tk.BooleanVar(value=False)

path_var = tk.StringVar(value="Downloads will be saved in the current folder")
settings_card = ttk.Frame(controls, style="Card.TFrame", padding=16)
settings_card.grid(row=1, column=0, sticky="nsew")
settings_card.columnconfigure(0, weight=1)
ttk.Label(settings_card, text="Preferences", style="Section.TLabel").grid(
    row=0, column=0, sticky="w", pady=(0, 8)
)
playlist_check = ttk.Checkbutton(
    settings_card,
    text="Download playlist",
    variable=playlist_var,
    style="Card.TCheckbutton",
)
playlist_check.grid(row=1, column=0, sticky="w")
audio_check = ttk.Checkbutton(
    settings_card,
    text="Audio only",
    variable=audio_var,
    style="Card.TCheckbutton",
)
audio_check.grid(row=2, column=0, sticky="w")
pathPicker = ttk.Button(
    settings_card,
    text="Choose download folder",
    command=select_download_path,
    style="Modern.TButton",
)
pathPicker.grid(row=3, column=0, sticky="ew", pady=(10, 5))
ttk.Label(
    settings_card,
    textvariable=path_var,
    style="Muted.TLabel",
    wraplength=250,
).grid(row=4, column=0, sticky="w", pady=(0, 10))
downloadBtn = ttk.Button(
    settings_card,
    text="Start download",
    command=download_button_clicked,
    style="Download.TButton",
)
downloadBtn.grid(row=5, column=0, sticky="ew")

log_card = ttk.Frame(content, style="Card.TFrame", padding=16)
log_card.grid(row=0, column=1, sticky="nsew")
log_card.columnconfigure(0, weight=1)
log_card.rowconfigure(2, weight=1)
ttk.Label(log_card, text="Activity", style="Section.TLabel").grid(
    row=0, column=0, sticky="w"
)
ttk.Label(
    log_card,
    text="Download progress and messages appear here",
    style="Muted.TLabel",
).grid(row=1, column=0, sticky="w", pady=(3, 10))
logBar = ScrolledText(
    log_card,
    width=50,
    height=18,
    state="disabled",
    wrap=tk.WORD,
    bg=colors["field"],
    fg=colors["text"],
    insertbackground=colors["text"],
    selectbackground=colors["accent_hover"],
    relief="flat",
    borderwidth=0,
    padx=10,
    pady=10,
    font=("Consolas", 9),
)
logBar.grid(row=2, column=0, sticky="nsew")
clearLogBtn = ttk.Button(
    log_card,
    text="Clear activity",
    command=clear_log_clicked,
    style="Modern.TButton",
)
clearLogBtn.grid(row=3, column=0, sticky="e", pady=(10, 0))

root.mainloop()

