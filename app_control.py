import os
import subprocess


# =========================
# APPLICATIONS
# =========================

APPS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "chrome": "chrome.exe",
    "edge": "msedge.exe",
    "spotify": "spotify.exe",
    "vs code": "Code.exe",
    "vscode": "Code.exe",
}


# =========================
# OPEN APPLICATION
# =========================

def open_app(app_name, speak):

    app_name = app_name.lower().strip()

    if app_name not in APPS:
        speak(f"I don't know how to open {app_name}")
        return

    try:

        subprocess.Popen(APPS[app_name])

        speak(f"Opening {app_name}")

    except Exception as e:

        print("Open App Error:", e)

        speak(f"Sorry, I could not open {app_name}")


# =========================
# CLOSE APPLICATION
# =========================

def close_app(app_name, speak):

    app_name = app_name.lower().strip()

    if app_name not in APPS:    
        speak(f"I don't know how to close {app_name}")
        return

    process_name = APPS[app_name]

    try:

        os.system(
            f'taskkill /f /im "{process_name}" >nul 2>&1'
        )

        speak(f"Closing {app_name}")

    except Exception as e:

        print("Close App Error:", e)

        speak(f"Sorry, I could not close {app_name}")