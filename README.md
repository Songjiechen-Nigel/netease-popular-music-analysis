# 🎵 NetEase Music Trend Analyzer

A comprehensive project for scraping, analyzing, and processing music data from **NetEase Cloud Music (网易云音乐)**. This toolkit helps you explore popularity trends, extract musical features, and even download songs.

---

## 📦 Features

### 1. Scrape & Analyze Trends (`netease_music_scraper.py`)
- Scrape song metadata from the **Rising Chart**
- Fetch **popularity**, **comment counts**, and **top-liked comments**
- Visualize:
  - Song popularity (bar chart)
  - Comment engagement (scatter plot)

### 2. Download Songs (`NetEase_song_download.py`)
- Download a song using its NetEase Cloud Music ID
- Save it as an MP3
- Automatically name the file based on metadata

### 3. Audio Analysis (`bpm_key_detect.py`)
- Detect **BPM (tempo)** and **musical key** of a song using audio analysis
- Useful for DJs, remix artists, or musicologists

### 4. Audio Analysis (`music_sp_5stems.py`)
- Separate the audio to instruments and vocals to the specific folder
- vocals, drums, bass, piano, and other


# Install dependencies

requests
json
os
numpy
spleeter
librosa
soundfile 
time
matplotlib.pyplot
seaborn