# 🎥 Maldix YouTube Downloader

A sleek, professional CLI-based tool for downloading individual YouTube videos or entire channels. Built with Python, `yt-dlp`, and `rich` for a beautiful terminal experience.

## ✨ Features

- **Channel Support:** Automatically detects and downloads every video from a channel URL.
- **Forced MP4:** Ensures all downloads are merged into a high-quality `.mp4` container.
- **Smart Skip:** Uses `ignoreerrors` to skip private, deleted, or region-locked videos without crashing.
- **Clean UI:** Features live progress bars, download speeds, and estimated time remaining.
- **Auto-Organization:** Automatically sorts downloads into folders named after the uploader/channel.

---

## 🛠️ Prerequisites

Before running the script, you need to have the following installed on your system:

1.  **Python 3.7+**
2.  **FFmpeg:** Required for merging high-quality video and audio streams.
    * **Windows:** `winget install ffmpeg`
    * **macOS:** `brew install ffmpeg`
    * **Linux:** `sudo apt install ffmpeg`

---

## 🚀 Installation

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/Maldix-Youtube-Downloader.git](https://github.com/YOUR_USERNAME/Maldix-Youtube-Downloader.git)
    cd Maldix-Youtube-Downloader
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## 📖 Usage

1.  Run the application:
    ```bash
    python main.py
    ```
2.  Paste the URL of a **single video** or a **full channel**.
3.  The files will be saved in the `Maldix_Downloads/` folder, organized by channel name.

---

## 📂 Project Structure

* `main.py` — The core application logic.
* `requirements.txt` — Python library dependencies (`yt-dlp`, `rich`).
* `.gitignore` — Prevents large video files and binaries from being uploaded to GitHub.
* `README.md` — Project documentation.

---

## 📜 License

This project is open-source. Feel free to fork, modify, and use it for your own personal projects.

**Disclaimer:** This tool is for educational purposes only. Please respect YouTube's Terms of Service and the copyrights of content creators.
