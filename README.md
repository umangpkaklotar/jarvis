# 🎙️ JARVIS - AI Voice Assistant in Python

A smart voice-controlled personal assistant built using **Python**. JARVIS can understand voice commands, open websites, launch applications, play music, search YouTube, send WhatsApp messages, read the latest news, take screenshots, and perform various Windows system operations.

---

# 📌 Overview

JARVIS is a desktop voice assistant that uses speech recognition to listen to the user's voice and executes commands based on the spoken input.

The assistant is capable of performing everyday tasks like opening websites, searching YouTube, playing music, sending WhatsApp messages, opening Windows applications, taking screenshots, checking the current time, reading the latest news, and controlling some system functions.

---

# ✨ Main Features

## 🌐 Website Commands

- Open Google
- Open YouTube
- Open Facebook
- Open GitHub
- Open LinkedIn

---

## 🎵 Music Features

- Play songs from custom music library
- Automatically search YouTube if song is not available

Example:

```
Play believer
Play kesariya
```

---

## 🔍 YouTube Search

Example:

```
Search YouTube Python Tutorial
```

---

## 📱 WhatsApp Messaging

Send WhatsApp messages using voice commands.

Flow:

- Speak contact name
- Speak message
- Message sent automatically

---

## 📰 Latest News

Fetches the latest Indian news using **NewsAPI**.

Example:

```
Today's News
```

---

## 🕒 Date & Time

Ask current time.

Example:

```
What is the time
```

---

## 📷 Screenshot

Capture and save screenshots.

Example:

```
Take Screenshot
```

Screenshot is automatically saved as

```
screenshot.png
```

---

## 💻 Windows Applications

Open

- Notepad
- Calculator
- Paint

---

## 🔒 System Commands

- Shutdown Computer
- Cancel Shutdown
- Lock Computer

---

## 🎤 Speech Recognition

Uses Google Speech Recognition API.

Supports microphone detection automatically.

---

# 🛠 Technologies Used

- Python 3.x
- SpeechRecognition
- PyAudio
- Pyttsx3
- PyWhatKit
- Requests
- PyAutoGUI
- Webbrowser
- OS
- Datetime
- Platform
- Ctypes
- NewsAPI

---

# 📂 Project Structure

```
JARVIS/
│
├── main.py
├── musicLibrary.py
├── screenshot.png
├── PyWhatKit_DB.txt
├── static/
├── templates/
├── venv/
└── README.md
```

---

# 📦 Requirements

Install dependencies

```bash
pip install SpeechRecognition
pip install PyAudio
pip install pyttsx3
pip install pywhatkit
pip install requests
pip install pyautogui
```

Or

```bash
pip install -r requirements.txt
```

---

# ▶️ Run Project

```bash
python main.py
```

---

# 🎤 Available Voice Commands

## Websites

```
Open Google
Open YouTube
Open GitHub
Open LinkedIn
Open Facebook
```

---

## Music

```
Play believer
Play kesariya
```

---

## YouTube

```
Search YouTube Python Tutorial
```

---

## WhatsApp

```
Send WhatsApp Message
```

---

## Screenshot

```
Take Screenshot
```

---

## Time

```
What is the time
```

---

## News

```
Today's News
```

---

## Applications

```
Open Notepad
Open Calculator
Open Paint
```

---

## System

```
Shutdown Computer

Cancel Shutdown

Lock Computer
```

---

# 🎵 Custom Music Library

Songs are stored inside

```
musicLibrary.py
```

Example

```python
music = {
    "believer": "YouTube Link",
    "kesariya": "YouTube Link"
}
```

---

# 🔑 API Used

## News API

Website

https://newsapi.org/

Used for

- Latest Headlines
- India News

---

# ⚙️ Future Improvements

- ChatGPT Integration
- Gemini AI Integration
- Weather Forecast
- Email Assistant
- Face Recognition Login
- Object Detection
- OCR
- AI Chat Mode
- Voice Authentication
- Volume Control
- Brightness Control
- Battery Percentage
- Internet Speed Test
- Reminder System
- Alarm
- Calendar
- AI Conversation Mode

---

# 📸 Screenshots

Add screenshots of the project here.

Example

```
screenshot.png
```

---

# 👨‍💻 Author

**Umang P Kaklotar**

GitHub:
https://github.com/umangpkaklotar

LinkedIn:
https://www.linkedin.com/in/your-linkedin-profile/

---

# 📄 License

This project is developed for learning and educational purposes.

Feel free to fork, modify, and improve it.

⭐ Don't forget to give this repository a Star if you like this project.
