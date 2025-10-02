import os
import tkinter as tk
from tkinter import filedialog, messagebox
from yt_dlp import YoutubeDL
from pydub import AudioSegment
import threading

def convert_audio(input_path, output_path):
    """Convert audio to desired format and remove original file"""
    audio = AudioSegment.from_file(input_path)
    audio.export(output_path, format=os.path.splitext(output_path)[1][1:])
    os.remove(input_path)

def download_audio(url, folder, format_choice):
    try:
        os.makedirs(folder, exist_ok=True)

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(folder, "%(title)s.%(ext)s"),
            "quiet": True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            downloaded_file = ydl.prepare_filename(info)

        base, ext = os.path.splitext(downloaded_file)
        output_file = f"{base}.{format_choice}"

        # Convert if needed
        if ext[1:] != format_choice:
            convert_audio(downloaded_file, output_file)

        messagebox.showinfo("Success", f"Audio downloaded to:\n{folder}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def browse_folder():
    folder = filedialog.askdirectory()
    folder_var.set(folder)

def start_download():
    url = url_entry.get().strip()
    folder = folder_var.get().strip()
    fmt = format_var.get()
    if not url or not folder:
        messagebox.showerror("Error", "Please enter a URL and choose a folder")
        return
    threading.Thread(target=download_audio, args=(url, folder, fmt)).start()

# === GUI Setup ===
root = tk.Tk()
root.title("YouTube Audio Downloader & Converter")
root.geometry("550x250")

tk.Label(root, text="YouTube URL:").pack(pady=5)
url_entry = tk.Entry(root, width=70)
url_entry.pack(pady=5)

folder_var = tk.StringVar()
tk.Entry(root, textvariable=folder_var, width=70).pack(pady=5)
tk.Button(root, text="Browse Folder", command=browse_folder).pack(pady=5)

format_var = tk.StringVar(value="mp3")
tk.Label(root, text="Audio Format:").pack(pady=5)
tk.OptionMenu(root, format_var, "mp3", "wav").pack(pady=5)

tk.Button(root, text="Download & Convert", command=start_download, width=30, height=2).pack(pady=15)

root.mainloop()