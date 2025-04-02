# 🎬 Video Trim & Subtitle Tool

A web application for trimming videos with an interactive range slider and managing subtitles.

---

## 🚀 **Table of Contents**
1. [Project Description](#-project-description)
2. [Features](#-features)
3. [Requirements](#-requirements)
4. [Installation](#-installation)
5. [Configuration](#-configuration)
6. [Usage](#-usage)
7. [Screenshots](#-screenshots)
8. [Known Issues](#-known-issues)
9. [Authors](#-authors)
10. [License](#-license)

---

## 📖 **Project Description**

A web tool for viewing videos, trimming videos using a range slider and managing subtitles. 

---

## ✨ **Features**

- Dynamic display of subtitles for the selected video segment.
- WebSocket support 
- Intuitive control panel (`Start`, `Stop`, `Rewind`, `Cut`).
- Interactive slider for trimming videos within a specified time range.
- Wisualize subtitles in trim range
- Save trimmed video with subtitles and audio
- Video viewer in thread
- Generate transcription using Whisper-AI (working in independent thread)

---

## 🛠️ **Requirements**

- **Backend:** Python 3.x (e.g., with Flask) or Node.js  
- **Frontend:** HTML, CSS, JavaScript  
- **Libraries:** noUiSlider, Bootstrap v5.2.3

### 🔹 **FFmpeg**
Required for video and audio processing
  - On **Windows**, example to add `ffmpeg/bin` to your system's PATH in VSC:
    ```powershell
    $env:PATH += ";D:\ffmpeg\bin"
    ```
  - On **Linux**, set the `LD_LIBRARY_PATH` to include the necessary libraries in VSC:
    ```bash
    export LD_LIBRARY_PATH=/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu
    ```

### 🔹 **Python Dependencies**
Install the required libraries using:
```sh
pip install -r requirements.txt
```

## 📷 **Screenshots**



![1](https://github.com/user-attachments/assets/5d9aab88-e6c1-43d0-a7e0-9fee78e5ff35)


![2](https://github.com/user-attachments/assets/f1567af3-672c-47d3-8f32-25d43147d94f)


![3](https://github.com/user-attachments/assets/2f77acdb-ae68-49f7-97d3-231e86fd3047)


![4](https://github.com/user-attachments/assets/38be5c1f-dd5e-4bdc-b0e1-2ddea8587929)

