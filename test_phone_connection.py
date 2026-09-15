import os
import sys
import socket
import requests
from dotenv import load_dotenv

load_dotenv()

PHONE_IP = os.getenv("PHONE_IP")
PHONE_PORT = os.getenv("PHONE_PORT", "8080")
PHONE_TOKEN = os.getenv("PHONE_TOKEN")

print(f"--- Jarvis Phone Diagnostic Test ---")
print(f"Loaded PHONE_IP: {PHONE_IP}")
print(f"Loaded PHONE_PORT: {PHONE_PORT}")
print(f"Token is configured: {bool(PHONE_TOKEN)}")

if not PHONE_IP:
    print("Error: PHONE_IP is missing in .env")
    sys.exit(1)

print(f"\n1. Testing raw TCP connection to {PHONE_IP}:{PHONE_PORT}...")
try:
    with socket.create_connection((PHONE_IP, int(PHONE_PORT)), timeout=3) as sock:
        print("Success! TCP Connection established (Port is open and listening).")
except ConnectionRefusedError:
    print("Error: Connection Refused. The Android app is likely NOT RUNNING, or it failed to start the server.")
    sys.exit(1)
except socket.timeout:
    print("Error: Connection Timed Out. Your PC cannot reach the phone over the network (check Wi-Fi or AP isolation).")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

print(f"\n2. Testing HTTP /status endpoint...")
url = f"http://{PHONE_IP}:{PHONE_PORT}/status"
headers = {"Authorization": f"Bearer {PHONE_TOKEN}"}
try:
    resp = requests.get(url, headers=headers, timeout=3)
    print(f"Status Code: {resp.status_code}")
    print(f"Response Body: {resp.text}")
except Exception as e:
    print(f"HTTP Error: {e}")

print("\nDiagnostic complete.")
