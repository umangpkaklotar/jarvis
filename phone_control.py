import os
import requests
from dotenv import load_dotenv

load_dotenv()

PHONE_IP = os.getenv("PHONE_IP", "")
PHONE_PORT = os.getenv("PHONE_PORT", "8080")
PHONE_TOKEN = os.getenv("PHONE_TOKEN", "")

def _get_base_url():
    if not PHONE_IP:
        return None
    return f"http://{PHONE_IP}:{PHONE_PORT}"

def _get_headers():
    return {
        "Authorization": f"Bearer {PHONE_TOKEN}",
        "Content-Type": "application/json"
    }

def check_connection() -> dict:
    url = _get_base_url()
    print(f"[phone_control] check_connection called. URL: {url}")
    if not url:
        print("[phone_control] Error: Phone IP is not configured in .env.")
        return {"success": False, "message": "Phone IP is not configured in .env."}
    
    try:
        print(f"[phone_control] Sending GET request to {url}/status")
        response = requests.get(f"{url}/status", headers=_get_headers(), timeout=5)
        print(f"[phone_control] Received response with status code: {response.status_code}")
        if response.status_code == 401:
            return {"success": False, "message": "Authentication failed. Invalid token."}
        if response.status_code == 200:
            return response.json()
        return {"success": False, "message": f"Server returned error code {response.status_code}"}
    except requests.exceptions.RequestException as e:
        print(f"[phone_control] RequestException occurred: {e}")
        return {"success": False, "message": "I can't connect to your phone. Please make sure the Jarvis Phone app is running and both devices are connected to the same Wi-Fi."}


def open_phone_app(app_name: str) -> dict:
    url = _get_base_url()
    if not url:
        return {"success": False, "message": "Phone IP is not configured in .env."}
    
    payload = {
        "action": "open_app",
        "target": app_name.lower()
    }
    
    try:
        print(f"[phone_control] Sending POST request to {url}/command for app: {app_name}")
        response = requests.post(f"{url}/command", json=payload, headers=_get_headers(), timeout=5)
        print(f"[phone_control] Received response with status code: {response.status_code}")
        if response.status_code == 401:
            return {"success": False, "message": "Authentication failed. Invalid token."}
        
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[phone_control] RequestException occurred: {e}")
        return {"success": False, "message": "I can't connect to your phone. Please make sure the Jarvis Phone app is running and both devices are connected to the same Wi-Fi."}
