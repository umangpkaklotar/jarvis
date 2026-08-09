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
    "google chrome": "chrome.exe",
    "edge": "msedge.exe",
    "microsoft edge": "msedge.exe",
    "firefox": "firefox.exe",
    "spotify": "spotify.exe",
    "vs code": "Code.exe",
    "vscode": "Code.exe",
    "visual studio code": "Code.exe",
    "file explorer": "explorer.exe",
    "explorer": "explorer.exe",
    "task manager": "taskmgr.exe",
    "command prompt": "cmd.exe",
    "cmd": "cmd.exe",
    "powershell": "powershell.exe",
    "word": "WINWORD.exe",
    "excel": "EXCEL.exe",
    "powerpoint": "POWERPNT.exe",
    "vlc": "vlc.exe",
    "snipping tool": "SnippingTool.exe",
}

# Browser-based apps — these run inside a browser, not as separate processes
# Maps app name -> browser process to kill
BROWSER_APPS = {
    "youtube": "chrome.exe",
    "gmail": "chrome.exe",
    "whatsapp": "chrome.exe",
    "facebook": "chrome.exe",
    "instagram": "chrome.exe",
    "twitter": "chrome.exe",
    "linkedin": "chrome.exe",
    "github": "chrome.exe",
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

    # Check if it's a browser-based app (like YouTube)
    if app_name in BROWSER_APPS:
        process_name = BROWSER_APPS[app_name]
        try:
            result = os.system(
                f'taskkill /f /im "{process_name}" >nul 2>&1'
            )
            if result == 0:
                speak(f"Closing {app_name} by closing the browser")
                print(f"Closed browser ({process_name}) for {app_name}")
            else:
                speak(f"Could not find {app_name} running")
                print(f"No process found for {app_name} ({process_name})")
        except Exception as e:
            print("Close Browser App Error:", e)
            speak(f"Sorry, I could not close {app_name}")
        return

    if app_name not in APPS:
        speak(f"I don't know how to close {app_name}")
        print(f"App '{app_name}' not found in APPS or BROWSER_APPS dictionary")
        return

    process_name = APPS[app_name]

    try:

        result = os.system(
            f'taskkill /f /im "{process_name}" >nul 2>&1'
        )

        if result == 0:
            speak(f"Closing {app_name}")
            print(f"Closed {app_name} ({process_name})")
        else:
            speak(f"Could not find {app_name} running")
            print(f"No process found for {app_name} ({process_name})")

    except Exception as e:

        print("Close App Error:", e)

        speak(f"Sorry, I could not close {app_name}")