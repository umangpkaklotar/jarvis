import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import pywhatkit
import os
from datetime import datetime
import pyautogui
import ctypes
import platform
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
from app_control import AppController, parse_open_close_command, open_in_chrome
import phone_control


NEWS_API_KEY = "acdd2f2873824cb5a06d67ee3ad16fce"


recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Initialize the application/window controller
controller = AppController()


def get_microphone_index():
    try:
        import pyaudio
        p = pyaudio.PyAudio()
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount', 0)
        
        preferred_index = None
        fallback_index = None
        
        for i in range(0, numdevices):
            device_info = p.get_device_info_by_host_api_device_index(0, i)
            name = device_info.get('name', '')
            max_inputs = device_info.get('maxInputChannels', 0)
            
            if max_inputs > 0:
                name_lower = name.lower()
                is_virtual = "virtual" in name_lower or "mapper" in name_lower
                is_real_mic = ("microphone" in name_lower or "mic" in name_lower or "array" in name_lower or "audio" in name_lower) and not is_virtual
                
                if is_real_mic:
                    if "realtek" in name_lower or "amd" in name_lower or "array" in name_lower:
                        p.terminate()
                        return i
                    if preferred_index is None:
                        preferred_index = i
                elif fallback_index is None:
                    fallback_index = i
        p.terminate()
        if preferred_index is not None:
            return preferred_index
        return fallback_index
    except Exception:
        return None

mic_index = get_microphone_index()
if mic_index is not None:
    print(f"Using microphone device index: {mic_index}")
else:
    print("Using default microphone device index.")



def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
   c_lower = c.lower()

   # ------------------------------------------------------------------
   # 1) Intercept Phone Commands First
   # ------------------------------------------------------------------
   phone_phrases = ["on my phone", "on phone", "in my phone", "in phone"]
   is_phone_cmd = any(phrase in c_lower for phrase in phone_phrases)

   if "check my phone connection" in c_lower or "check phone connection" in c_lower:
       speak("Checking phone connection.")
       result = phone_control.check_connection()
       if result.get("success"):
           speak("Your phone is connected.")
       else:
           msg = result.get("message", "I cannot connect to your phone.")
           speak(msg)
       return False

   if is_phone_cmd and ("open" in c_lower or "launch" in c_lower or "start" in c_lower):
       # Extract app name
       cmd_clean = c_lower
       for phrase in phone_phrases:
           cmd_clean = cmd_clean.replace(phrase, "")
       cmd_clean = cmd_clean.replace("open", "").replace("launch", "").replace("start", "").strip()
       
       if not cmd_clean:
           speak("I didn't catch the app name to open on your phone.")
           return False

       speak(f"Opening {cmd_clean} on your phone.")
       result = phone_control.open_phone_app(cmd_clean)
       
       if not result.get("success"):
           msg = result.get("message", f"I could not open {cmd_clean} on your phone.")
           speak(msg)
       return False

   # ------------------------------------------------------------------
   # 2) Try the PC open/close handler next (websites + desktop apps)
   # ------------------------------------------------------------------
   if controller.handle_command(c, speak):
       return False


   # ------------------------------------------------------------------
   # 3) Existing commands (all preserved as-is, with voice confirmations)
   # ------------------------------------------------------------------

# date time
   if "time" in c_lower:
    current = datetime.now().strftime("%I:%M %p")
    speak(f"The time is {current}")

# screenshot 
   elif "take a screenshot" in c_lower:
    speak("Taking a screenshot.")
    image = pyautogui.screenshot()
    image.save(os.path.join(os.path.dirname(__file__), "screenshot.png"))
    speak("Screenshot saved.")

   elif "open desktop" in c_lower:
    speak("Opening Desktop.")
    os.startfile(r"C:\Users\Public\Desktop")
     
   elif "shutdown computer" in c_lower:
    speak("Shutting down computer.")
    os.system("shutdown /s /t 5")
    # cancel shutdown
   elif "cancel shutdown" in c_lower:
    os.system("shutdown /a")
    speak("Shutdown cancelled.")

# lock computer
   elif "lock computer" in c_lower:
    speak("Locking computer.")
    ctypes.windll.user32.LockWorkStation()

# news mate 
   elif "news" in c_lower:
    try:
        speak("Getting today's news.")

        url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=acdd2f2873824cb5a06d67ee3ad16fce"

        response = requests.get(url)

        data = response.json()

        print(data)   # <-- Add this
    

        articles = data["articles"]

        for article in articles[:5]:
            print(article["title"])
            speak(article["title"])

    except Exception as e:
        print(e)
        speak("Sorry, I could not get the news.")

# play music 
   elif "play" in c_lower:
    play_idx = c_lower.find("play")
    song = c[play_idx + 4:].strip().lower()

    if song in musicLibrary.music:
        speak(f"Playing {song}.")
        open_in_chrome(musicLibrary.music[song])
    else:
        speak(f"Playing {song}.")
        if not controller.play_on_youtube(song):
            speak("Sorry, I could not play that on YouTube.")
   
   
   elif "search youtube" in c_lower:
    query = c_lower.replace("search youtube", "").strip()
    speak(f"Searching YouTube for {query}.")
    open_in_chrome(f"https://www.youtube.com/results?search_query={query}")
   
        
   elif "send whatsapp message" in c_lower:
       speak("Sending WhatsApp message.")
       speak("Whom should I send the message to?")
       with sr.Microphone(device_index=mic_index) as source:
           print("Listening contact name...")
           audio = recognizer.listen(source)
           name = recognizer.recognize_google(audio).lower()
 
       contacts = {
           "jay": "+917043456789",
           "mom": "+919876543210",
           "vivek" : "+917573928352",
           "friend": "+918888888888"
       }
 
       if name in contacts:
           speak("What should I send?")
           with sr.Microphone(device_index=mic_index) as source:
               print("Listening message...")
               audio = recognizer.listen(source)
               message = recognizer.recognize_google(audio)
 
           pywhatkit.sendwhatmsg_instantly(
               contacts[name],
               message,
               wait_time=10
           )
           speak("Message sent.")
       else:
           speak("Contact not found.")
           
   elif "stop" in c_lower or "exit" in c_lower or "quit" in c_lower:
       speak("Goodbye.")
       controller.cleanup()
       return True
       
   return False

if __name__ == "__main__":
    speak("initializing jarvis...")
    
    print("Adjusting for ambient noise. Please stay silent for a moment...")
    try:
        with sr.Microphone(device_index=mic_index) as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
    except Exception as e:
        print(f"Warning: Could not adjust for ambient noise: {e}")
        
    speak("Jarvis is active and listening for your commands.")
    print("Jarvis is active and listening. Say 'stop' or 'exit' to quit.")
    
    while True:
        try:
            with sr.Microphone(device_index=mic_index) as source:
                print("\nListening for command...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            
            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            
            if processCommand(command):
                break
                    
        except sr.WaitTimeoutError:
            # Silent timeout is normal when not speaking
            continue
        except sr.UnknownValueError:
            # Could not recognize speech, continue listening
            continue
        except Exception as e:
            print(f"Error: {repr(e)}")
           
            