"""
app_control.py — Voice Feedback + Application/Window Control System for Jarvis.

Provides:
  - AppController: tracks opened browser tabs (via Selenium) and desktop apps
    (via subprocess), so individual tabs/apps can be closed on demand.
  - parse_open_close_command(): natural-language intent parser for open/close.
  - open_in_chrome(): backward-compatible helper used by existing main.py code.
"""

import subprocess
import time
import re
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    WebDriverException,
    NoSuchWindowException,
    InvalidSessionIdException,
    TimeoutException,
)

try:
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    ChromeDriverManager = None


# ---------------------------------------------------------------------------
# Registry: websites  (name -> URL)
# ---------------------------------------------------------------------------
WEBSITE_REGISTRY = {
    "youtube":   "https://www.youtube.com",
    "google":    "https://www.google.com",
    "facebook":  "https://www.facebook.com",
    "github":    "https://github.com",
    "linkedin":  "https://www.linkedin.com/feed/",
    "twitter":   "https://twitter.com",
    "x":         "https://twitter.com",
    "instagram": "https://www.instagram.com",
    "reddit":    "https://www.reddit.com",
    "stackoverflow": "https://stackoverflow.com",
    "stack overflow": "https://stackoverflow.com",
    "chatgpt":   "https://chat.openai.com",
    "chat gpt":  "https://chat.openai.com",
    "whatsapp web": "https://web.whatsapp.com",
    "amazon":    "https://www.amazon.in",
    "flipkart":  "https://www.flipkart.com",
    "netflix":   "https://www.netflix.com",
    "gmail":     "https://mail.google.com",
}

# ---------------------------------------------------------------------------
# Registry: desktop applications  (name -> (exe_command, process_image_name))
#   exe_command      : what to launch via subprocess / os.system
#   process_image_name : used to find the process for closing
# ---------------------------------------------------------------------------
APP_REGISTRY = {
    "notepad":     ("notepad.exe",        "notepad.exe"),
    "calculator":  ("calc.exe",           "CalculatorApp.exe"),
    "calc":        ("calc.exe",           "CalculatorApp.exe"),
    "paint":       ("mspaint.exe",        "mspaint.exe"),
    "wordpad":     ("wordpad.exe",        "wordpad.exe"),
    "cmd":         ("cmd.exe",            "cmd.exe"),
    "command prompt": ("cmd.exe",         "cmd.exe"),
    "powershell":  ("powershell.exe",     "powershell.exe"),
    "file explorer": ("explorer.exe",     "explorer.exe"),
    "explorer":    ("explorer.exe",       "explorer.exe"),
    "task manager": ("taskmgr.exe",       "Taskmgr.exe"),
    "snipping tool": ("SnippingTool.exe", "SnippingTool.exe"),
    # Apps that live in typical install paths
    "vs code":     (r'"C:\Users\{user}\AppData\Local\Programs\Microsoft VS Code\Code.exe"', "Code.exe"),
    "vscode":      (r'"C:\Users\{user}\AppData\Local\Programs\Microsoft VS Code\Code.exe"', "Code.exe"),
    "visual studio code": (r'"C:\Users\{user}\AppData\Local\Programs\Microsoft VS Code\Code.exe"', "Code.exe"),
    "spotify":     (r'"C:\Users\{user}\AppData\Roaming\Spotify\Spotify.exe"', "Spotify.exe"),
    "discord":     (r'"C:\Users\{user}\AppData\Local\Discord\Update.exe" --processStart Discord.exe', "Discord.exe"),
    "vlc":         (r'"C:\Program Files\VideoLAN\VLC\vlc.exe"', "vlc.exe"),
}

# Names that refer to the browser itself (not a website tab)
BROWSER_NAMES = {"chrome", "google chrome", "browser"}

# ---------------------------------------------------------------------------
# Natural-language intent parsing
# ---------------------------------------------------------------------------
_OPEN_VERBS  = ("open", "launch", "start", "run")
_CLOSE_VERBS = ("close", "exit", "quit", "stop", "kill", "end", "shut")


def parse_open_close_command(command: str):
    """Return (action, target_name) or (None, None).

    action is ``"open"`` or ``"close"``.
    target_name is the lowercased, stripped entity name.
    """
    text = command.lower().strip()

    # Remove filler words that speech recognition may add
    text = re.sub(r"\b(the|a|an|my|please|can you|could you|jarvis)\b", "", text).strip()
    # Remove trailing "tab" / "window" / "application" / "app"
    text = re.sub(r"\s+(tab|window|application|app)$", "", text).strip()

    for verb in _CLOSE_VERBS:
        pattern = rf"^{verb}\s+(.+)"
        m = re.match(pattern, text)
        if m:
            return ("close", m.group(1).strip())

    for verb in _OPEN_VERBS:
        pattern = rf"^{verb}\s+(.+)"
        m = re.match(pattern, text)
        if m:
            return ("open", m.group(1).strip())

    return (None, None)


def _resolve_user_path(path: str) -> str:
    """Replace ``{user}`` placeholder with the current username."""
    return path.replace("{user}", os.getlogin())


# ---------------------------------------------------------------------------
# Singleton reference so open_in_chrome() can reuse the controller's driver
# ---------------------------------------------------------------------------
_global_controller = None


class AppController:
    """Manages browser tabs (Selenium) and desktop apps (subprocess)."""

    def __init__(self):
        global _global_controller
        self._driver = None          # Selenium WebDriver (lazy init)
        self._tab_handles = {}       # name -> window handle
        self._app_processes = {}     # name -> subprocess.Popen
        _global_controller = self

    # ------------------------------------------------------------------
    # Selenium driver (lazy)
    # ------------------------------------------------------------------
    def _ensure_driver(self):
        """Start Chrome via Selenium if not already running."""
        if self._driver is not None:
            # Check the session is still alive
            try:
                _ = self._driver.current_url
                return
            except (WebDriverException, InvalidSessionIdException):
                self._driver = None

        opts = ChromeOptions()
        opts.add_argument("--start-maximized")
        opts.add_argument("--autoplay-policy=no-user-gesture-required")
        opts.add_experimental_option("excludeSwitches", ["enable-logging"])
        # Keep Chrome open even if driver object is GC'd
        opts.add_experimental_option("detach", True)

        try:
            if ChromeDriverManager is not None:
                service = ChromeService(ChromeDriverManager().install())
            else:
                service = ChromeService()
            self._driver = webdriver.Chrome(service=service, options=opts)
        except WebDriverException as exc:
            raise RuntimeError(f"Could not start Chrome: {exc}") from exc

    # ------------------------------------------------------------------
    # Website / tab management
    # ------------------------------------------------------------------
    def open_website(self, name: str, url: str | None = None) -> bool:
        """Open *name* in a new Chrome tab; track the handle.

        Returns True on success, False on failure.
        """
        key = name.lower()
        if url is None:
            url = WEBSITE_REGISTRY.get(key)
        if url is None:
            return False

        try:
            self._ensure_driver()
        except RuntimeError:
            return False

        # If we already have a tracked tab for this name, switch to it
        if key in self._tab_handles:
            try:
                self._driver.switch_to.window(self._tab_handles[key])
                self._driver.get(url)
                return True
            except (NoSuchWindowException, WebDriverException):
                # Tab was manually closed; open fresh
                del self._tab_handles[key]

        # Open a new tab
        try:
            self._driver.execute_script("window.open('');")
            new_handle = self._driver.window_handles[-1]
            self._driver.switch_to.window(new_handle)
            self._driver.get(url)
            self._tab_handles[key] = new_handle
            return True
        except WebDriverException:
            return False

    def close_website(self, name: str) -> str:
        """Close the tracked tab for *name*.

        Returns a status string: ``"closed"``, ``"not_found"``, ``"error"``.
        """
        key = name.lower()
        handle = self._tab_handles.get(key)
        if handle is None:
            return "not_found"

        try:
            self._driver.switch_to.window(handle)
            self._driver.close()
            del self._tab_handles[key]

            # Switch back to the last remaining tab (if any)
            remaining = self._driver.window_handles
            if remaining:
                self._driver.switch_to.window(remaining[-1])
            return "closed"
        except (NoSuchWindowException, WebDriverException):
            # Already gone
            self._tab_handles.pop(key, None)
            return "not_found"

    # ------------------------------------------------------------------
    # Desktop application management
    # ------------------------------------------------------------------
    def open_app(self, name: str) -> str:
        """Launch a desktop app by registry name.

        Returns: ``"opened"``, ``"already_open"``, ``"not_supported"``, ``"error"``.
        """
        key = name.lower()
        entry = APP_REGISTRY.get(key)
        if entry is None:
            return "not_supported"

        exe_cmd, _ = entry
        exe_cmd = _resolve_user_path(exe_cmd)

        # Check if we already have a tracked, running process
        proc = self._app_processes.get(key)
        if proc is not None and proc.poll() is None:
            return "already_open"

        try:
            proc = subprocess.Popen(exe_cmd, shell=True)
            self._app_processes[key] = proc
            return "opened"
        except Exception:
            return "error"

    def close_app(self, name: str) -> str:
        """Terminate the tracked process for *name*.

        Returns: ``"closed"``, ``"not_found"``, ``"error"``.
        """
        key = name.lower()
        entry = APP_REGISTRY.get(key)

        # First try our tracked process
        proc = self._app_processes.get(key)
        if proc is not None and proc.poll() is None:
            try:
                proc.terminate()
                proc.wait(timeout=5)
                del self._app_processes[key]
                return "closed"
            except Exception:
                pass

        # Fallback: kill by image name (catches apps opened outside Jarvis too)
        if entry is not None:
            _, image_name = entry
            try:
                result = subprocess.run(
                    ["taskkill", "/f", "/im", image_name],
                    capture_output=True, text=True, timeout=10,
                )
                self._app_processes.pop(key, None)
                if result.returncode == 0:
                    return "closed"
                return "not_found"
            except Exception:
                return "error"

        return "not_found"

    # ------------------------------------------------------------------
    # Browser-level close (close entire Chrome)
    # ------------------------------------------------------------------
    def close_browser(self) -> str:
        """Quit the Selenium-managed Chrome instance entirely."""
        if self._driver is not None:
            try:
                self._driver.quit()
            except Exception:
                pass
            self._driver = None
            self._tab_handles.clear()
            return "closed"
        return "not_found"

    # ------------------------------------------------------------------
    # Open a raw URL (backward compat for music, search, etc.)
    # ------------------------------------------------------------------
    def open_url(self, url: str, label: str = "") -> bool:
        """Open an arbitrary URL in a new Chrome tab (tracked under *label*)."""
        try:
            self._ensure_driver()
            self._driver.execute_script("window.open('');")
            new_handle = self._driver.window_handles[-1]
            self._driver.switch_to.window(new_handle)
            self._driver.get(url)
            if label:
                self._tab_handles[label.lower()] = new_handle
            return True
        except Exception:
            return False

    # ------------------------------------------------------------------
    # Play a song/video on YouTube (auto-click first result)
    # ------------------------------------------------------------------
    def play_on_youtube(self, query: str) -> bool:
        """Search YouTube for *query* and auto-play the first video result.

        Opens in Chrome via Selenium, finds the first video, navigates to it
        with autoplay=1, and uses JavaScript to force playback.
        Returns True on success.
        """
        search_url = f"https://www.youtube.com/results?search_query={query}"
        try:
            self._ensure_driver()

            # Open a new tab for the search
            self._driver.execute_script("window.open('');")
            new_handle = self._driver.window_handles[-1]
            self._driver.switch_to.window(new_handle)
            self._driver.get(search_url)

            # Wait for video results to load, then get the first video URL
            wait = WebDriverWait(self._driver, 10)
            first_video = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "ytd-video-renderer a#video-title")
                )
            )
            video_url = first_video.get_attribute("href")

            if video_url:
                # Append autoplay=1 to force playback
                separator = "&" if "?" in video_url else "?"
                video_url = f"{video_url}{separator}autoplay=1"
                self._driver.get(video_url)
            else:
                first_video.click()

            # Wait for the video player to appear, then force play via JS
            time.sleep(2)
            self._driver.execute_script("""
                // Try to click the play button if video is paused
                var playBtn = document.querySelector('.ytp-play-button');
                if (playBtn) {
                    var title = playBtn.getAttribute('title') || '';
                    if (title.toLowerCase().includes('play')) {
                        playBtn.click();
                    }
                }
                // Direct play via the <video> element
                var video = document.querySelector('video');
                if (video) {
                    video.play().catch(function(e) {});
                }
            """)

            # Track this tab under the query name so it can be closed later
            self._tab_handles[query.lower()] = new_handle
            return True
        except (TimeoutException, WebDriverException) as exc:
            print(f"play_on_youtube error: {exc}")
            return False
        except Exception as exc:
            print(f"play_on_youtube unexpected error: {exc}")
            return False

    # ------------------------------------------------------------------
    # Cleanup on exit
    # ------------------------------------------------------------------
    def cleanup(self):
        """Gracefully close the Selenium browser."""
        try:
            if self._driver:
                self._driver.quit()
        except Exception:
            pass
        self._driver = None
        self._tab_handles.clear()

    # ------------------------------------------------------------------
    # High-level handler called from main.py
    # ------------------------------------------------------------------
    def handle_command(self, command: str, speak_fn) -> bool:
        """Try to handle an open/close command.

        Returns True if the command was handled, False otherwise.
        """
        action, target = parse_open_close_command(command)
        if action is None:
            return False

        target_key = target.lower()

        # Normalise some speech-recognition quirks
        alias_map = {
            "git hub": "github",
            "linked in": "linkedin",
            "what's app": "whatsapp web",
            "whatsapp": "whatsapp web",
            "face book": "facebook",
            "you tube": "youtube",
            "v s code": "vs code",
            "vs code": "vs code",
            "visual studio code": "vs code",
            "v l c": "vlc",
        }
        target_key = alias_map.get(target_key, target_key)
        display_name = target.title()

        # ----- OPEN -------------------------------------------------
        if action == "open":
            # Browser itself?
            if target_key in BROWSER_NAMES:
                speak_fn(f"Opening {display_name}.")
                try:
                    self._ensure_driver()
                    return True
                except RuntimeError:
                    speak_fn(f"Sorry, I could not open {display_name}.")
                    return True

            # Known website?
            if target_key in WEBSITE_REGISTRY:
                speak_fn(f"Opening {display_name}.")
                if self.open_website(target_key):
                    return True
                else:
                    speak_fn(f"Sorry, I could not open {display_name}.")
                    return True

            # Known desktop app?
            if target_key in APP_REGISTRY:
                result = self.open_app(target_key)
                if result == "opened":
                    speak_fn(f"Opening {display_name}.")
                elif result == "already_open":
                    speak_fn(f"{display_name} is already open.")
                else:
                    speak_fn(f"Sorry, I could not open {display_name}.")
                return True

            # Unknown target — not handled
            return False

        # ----- CLOSE ------------------------------------------------
        if action == "close":
            # Browser itself?
            if target_key in BROWSER_NAMES:
                speak_fn(f"Closing {display_name}.")
                self.close_browser()
                return True

            # Known website?
            if target_key in WEBSITE_REGISTRY:
                status = self.close_website(target_key)
                if status == "closed":
                    speak_fn(f"Closing {display_name}.")
                else:
                    speak_fn(f"I could not find an open {display_name} tab.")
                return True

            # Known desktop app?
            if target_key in APP_REGISTRY:
                status = self.close_app(target_key)
                if status == "closed":
                    speak_fn(f"Closing {display_name}.")
                elif status == "not_found":
                    speak_fn(f"I could not find {display_name} open.")
                else:
                    speak_fn(f"Sorry, I could not close {display_name}.")
                return True

            return False

        return False


# ---------------------------------------------------------------------------
# Backward-compatible helper — called by existing main.py code
# ---------------------------------------------------------------------------
def open_in_chrome(url: str):
    """Open a URL via the global AppController (or fall back to webbrowser)."""
    if _global_controller is not None:
        _global_controller.open_url(url)
    else:
        import webbrowser
        webbrowser.open(url)
