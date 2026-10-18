# 🤖 JARVIS — AI Voice Assistant

> A smart, voice-controlled personal assistant built with **Python** that listens, understands, and executes commands hands-free.

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/License-Educational-green)](LICENSE)

---

## 📌 Overview

JARVIS is a desktop voice assistant that uses **Google Speech Recognition** to listen to your voice and execute commands in real time. It can open websites, play music, send WhatsApp messages, read the latest news, take screenshots, control system functions, and much more — all through natural voice commands.

---

## ✨ Features at a Glance

| Category               | Commands                                                          |
| ---------------------- | ----------------------------------------------------------------- |
| 🌐 **Websites**       | Google, YouTube, Facebook, GitHub, LinkedIn                       |
| 🎵 **Music**          | Play from library or auto-search YouTube                          |
| 🔍 **YouTube Search** | Search any query directly on YouTube                              |
| 📱 **WhatsApp**       | Send messages via voice to saved contacts                         |
| 📰 **News**           | Fetch latest Indian headlines via NewsAPI                         |
| 🌤️ **Weather**       | Get real-time weather for any city (Open-Meteo API)               |
| 🕒 **Time**           | Ask the current time                                              |
| 📷 **Screenshot**     | Capture and save a screenshot                                     |
| 💻 **Applications**   | Open Notepad, Calculator, Paint                                   |
| 🔒 **System**         | Shutdown, Cancel Shutdown, Lock Computer                          |

---

## 🚀 How It Works — Application Flow

```
┌─────────────────────────────────────┐
│     Start: python backend/main.py   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Initialize TTS Engine (pyttsx3)    │
│  Detect Microphone (PyAudio)        │
│  Adjust for Ambient Noise           │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  🎤 Listening Loop Starts          │
│  Waits for voice input              │
│  (timeout: 5s, phrase limit: 8s)    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Google Speech Recognition          │
│  Converts audio → text command      │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  processCommand(command)            │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ Match against known commands: │  │
│  │  • "open google"              │  │
│  │  • "play <song>"             │  │
│  │  • "news"                     │  │
│  │  • "take a screenshot"       │  │
│  │  • "send whatsapp message"   │  │
│  │  • "shutdown computer"       │  │
│  │  • "stop" / "exit"           │  │
│  └───────────────────────────────┘  │
└──────────────┬──────────────────────┘
               │
        ┌──────┴──────┐
        │             │
        ▼             ▼
   ┌─────────┐  ┌───────────┐
   │ Execute │  │ "stop" /  │
   │ Command │  │ "exit"    │
   └────┬────┘  └─────┬─────┘
        │             │
        ▼             ▼
  Loop back      Speak "Goodbye"
  to listen      & Exit Program
```

---

## 📂 Project Structure

```
jarvis/
├── frontend/               # React + Vite activation UI
│   ├── public/
│   ├── src/                 # React app, original styles and activation behavior
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── backend/                # Existing Python voice assistant
│   ├── main.py
│   ├── app_control.py
│   ├── phone_control.py
│   ├── weather.py
│   ├── musicLibrary.py
│   ├── modules/
│   ├── requirements.txt
│   └── .env                 # Local configuration (not committed)
├── jarvis_phone/            # Existing Android phone-control app
├── .gitignore
└── README.md
```

The React interface preserves the existing browser-based activation greeting. The Python voice assistant runs separately; the existing project does not include an HTTP API connecting the two applications.

---

## 📦 Installation

### Prerequisites

- **Python 3.10+** installed
- **Node.js 18+** and npm installed
- **Windows OS** (uses Windows-specific system commands)
- A working **microphone**

### Steps

**1. Clone the repository**

```bash
git clone https://github.com/umangpkaklotar/jarvis.git
cd jarvis
```

**2. Create and activate a Python virtual environment (PowerShell)**

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**3. Install dependencies**

```bash
pip install -r backend/requirements.txt
```

**4. Run the assistant**

```bash
python backend/main.py
```

**5. Start the React + Vite frontend** (in a second terminal)

```powershell
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite. To create a production frontend build, run `npm run build` from `frontend/`.

The Python assistant and frontend are separate processes: start the Python voice loop with `python backend/main.py` from the repository root, and start Vite separately as above. No frontend-to-Python API is currently defined.

---

## 🎤 Voice Commands Reference

### 🌐 Open Websites

```
"Open Google"
"Open YouTube"
"Open Facebook"
"Open GitHub"
"Open LinkedIn"
```

### 🎵 Play Music

```
"Play believer"
"Play kesariya"
"Play tarak mehta"
```

> Songs are looked up in `musicLibrary.py` first. If not found, JARVIS auto-searches YouTube.

### 🔍 Search YouTube

```
"Search YouTube Python Tutorial"
```

### 📱 Send WhatsApp Message

```
"Send WhatsApp Message"
```

> JARVIS will ask for the **contact name** and then the **message** via voice.

### 📰 News

```
"Today's News"
"News"
```

### 🕒 Time

```
"What is the time"
"Time"
```

### 📷 Screenshot

```
"Take a Screenshot"
```

> Saved as `backend/screenshot.png`.

### 💻 Applications

```
"Open Notepad"
"Open Calculator"
"Open Paint"
"Open Desktop"
```

### 🔒 System Control

```
"Shutdown Computer"     — Shuts down in 5 seconds
"Cancel Shutdown"       — Cancels pending shutdown
"Lock Computer"         — Locks the workstation
```

### ❌ Exit

```
"Stop"
"Exit"
"Quit"
```

---

## 🎵 Custom Music Library

Edit [backend/musicLibrary.py](backend/musicLibrary.py) to add your own songs:

```python
music = {
    "song_name": "https://youtube.com/link",
    "believer": "https://youtu.be/...",
    "kesariya": "https://youtu.be/...",
}
```

---

## 🔑 APIs Used

| API                                              | Purpose                    |
| ------------------------------------------------ | -------------------------- |
| [NewsAPI](https://newsapi.org/)                   | Latest Indian headlines    |
| [Open-Meteo](https://open-meteo.com/)             | Real-time weather data     |
| [Google Speech Recognition](https://cloud.google.com/speech-to-text) | Voice to text conversion   |

---

## 🛠️ Tech Stack

| Technology         | Purpose                       |
| ------------------ | ----------------------------- |
| Python 3.x         | Core language                 |
| SpeechRecognition   | Voice input processing        |
| PyAudio             | Microphone access             |
| pyttsx3             | Text-to-speech output         |
| PyWhatKit           | WhatsApp & YouTube automation |
| Requests            | HTTP API calls                |
| PyAutoGUI           | Screenshot capture            |
| ctypes              | Windows system control        |

---

## ⚙️ Future Improvements

- [ ] ChatGPT / Gemini AI Integration
- [ ] Weather Forecast (extend current module)
- [ ] Email Assistant
- [ ] Face Recognition Login
- [ ] Object Detection & OCR
- [ ] Voice Authentication
- [ ] Volume & Brightness Control
- [ ] Battery Percentage & Internet Speed Test
- [ ] Reminder System, Alarm & Calendar
- [ ] Flask/FastAPI Web Dashboard

---

## 👨‍💻 Author

**Umang P Kaklotar**

- 🔗 GitHub: [umangpkaklotar](https://github.com/umangpkaklotar)
- 🔗 LinkedIn: [linkedin.com/in/umangpkaklotar](https://www.linkedin.com/in/your-linkedin-profile/)

---

## 📄 License

This project is developed for **learning and educational purposes**.
Feel free to fork, modify, and improve it.

⭐ **Star this repository** if you found it useful!

---

## 📱 JARVIS Phone Control Setup Guide

1. Connect your PC and Android phone to the **same Wi-Fi network** (e.g. 192.168.1.x).
2. Open the **JARVIS Phone** app on your Android device.
3. The Android app will display its IP address on the screen.
4. Copy that IP address.
5. Open `backend/.env` on your PC.
6. Set `PHONE_IP=<phone IP shown in Android app>` in `backend/.env`.
7. Ensure `PHONE_PORT=8080`.
8. Ensure `PHONE_TOKEN` matches the secure token configured in the Android app.
9. Start Jarvis using: `python backend/main.py` from the repository root.
10. Say: **"Check my phone connection"**
11. Jarvis will verbally confirm if the connection is successful!
