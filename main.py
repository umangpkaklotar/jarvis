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
import weather
import app_control

# Set Chrome as the default browser for all URL opens
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if os.path.exists(chrome_path):
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
    chrome_browser = webbrowser.get('chrome')
    print("Chrome browser registered successfully.")
else:
    chrome_browser = None
    print("Warning: Chrome not found. Using default browser.")

def open_in_chrome(url):
    """Open a URL in Chrome. Falls back to default browser if Chrome not found."""
    if chrome_browser:
        chrome_browser.open(url)
    else:
        webbrowser.open(url)

NEWS_API_KEY = "acdd2f2873824cb5a06d67ee3ad16fce"


recognizer = sr.Recognizer()
engine = pyttsx3.init()



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
   if "open google" in c_lower:
       speak("Opening Google")
       open_in_chrome("https://www.google.com")
   elif "open youtube" in c_lower:
       speak("Opening YouTube")
       open_in_chrome("https://www.youtube.com")
   elif "open facebook" in c_lower:
       speak("Opening Facebook")
       open_in_chrome("https://www.facebook.com")
   elif (
        "open github" in c_lower or
        "open git hub" in c_lower or
        "github" in c_lower):
        speak("Opening GitHub")
        open_in_chrome("https://github.com/umangpkaklotar?tab=repositories")
        
   elif "open linkedin" in c_lower:
        speak("Opening LinkedIn")
        open_in_chrome("https://www.linkedin.com/feed/")
  
   elif c_lower.startswith("open "):
       app_name = c_lower.replace("open ", "", 1).strip()
       if app_name in app_control.APPS:
           app_control.open_app(app_name, speak)
       else:
           speak(f"I don't know how to open {app_name}")

   elif c_lower.startswith("close "):
       app_name = c_lower.replace("close ", "", 1).strip()
       if app_name in app_control.APPS or app_name in app_control.BROWSER_APPS:
           app_control.close_app(app_name, speak)
       else:
           speak(f"I don't know how to close {app_name}")
           print(f"Unknown app to close: '{app_name}'")
# date time

   elif "time" in c_lower:
    current = datetime.now().strftime("%I:%M %p")
    speak(f"The time is {current}")

# screenshot 
   elif "take a screenshot" in c_lower:
    speak("Take a Screenshot")
    image = pyautogui.screenshot()
    image.save("screenshot.png")
    speak("Screenshot Saved")

    # application commands
   elif "open notepad" in c_lower:
        os.system("notepad")
   
   elif "open desktop" in c_lower:
    speak("Opening Desktop")
    os.startfile(r"C:\Users\Public\Desktop")
    
   elif "shutdown computer" in c_lower:
    speak("Shutting down computer")
    os.system("shutdown /s /t 5")
    # cancel shutdown
   elif "cancel shutdown" in c_lower:
    os.system("shutdown /a")
    speak("Shutdown cancelled")

# lock computer
   elif "lock computer" in c_lower:
    speak("Lock Computer")
    ctypes.windll.user32.LockWorkStation()

   elif "open calculator" in c_lower:
    os.system("calc")

   elif "open paint" in c_lower:
    os.system("mspaint")
   
# news mate 
   elif "news" in c_lower:
    try:
        speak("Getting today's news")

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
        speak(f"Playing {song}")
        open_in_chrome(musicLibrary.music[song])
    else:
        speak("Song not found in library. Playing from YouTube.")
        pywhatkit.playonyt(song)
   
   
   elif "search youtube" in c_lower:
    query = c_lower.replace("search youtube", "").strip()
    speak(f"Searching YouTube for {query}")
    open_in_chrome(f"https://www.youtube.com/results?search_query={query}")
   
        
   elif "send whatsapp message" in c_lower:
       speak("Whom should I send the message to")
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
           speak("What should I send")
           with sr.Microphone(device_index=mic_index) as source:
               print("Listening message...")
               audio = recognizer.listen(source)
               message = recognizer.recognize_google(audio)
 
           pywhatkit.sendwhatmsg_instantly(
               contacts[name],
               message,
               wait_time=10
           )
           speak("Message sent")
       else:
           speak("Contact not found")
           
   elif "stop" in c_lower or "exit" in c_lower or "quit" in c_lower:
       speak("Goodbye")
       return True
   
#  ============= weather command =================
   elif "weather" in c_lower:
       # Extract city name from various command patterns
       city = c_lower.replace("what is the weather in", "")
       city = city.replace("what's the weather in", "")
       city = city.replace("weather in", "")
       city = city.replace("weather at", "")
       city = city.replace("weather of", "")
       city = city.replace("weather", "")
       city = city.replace("?", "")
       city = city.strip()

       print(f"Weather command detected. City extracted: '{city}'")

       if city:
           weather.get_weather(city, speak)
       else:
           speak("Please say the city name. For example, say weather in Surat.")


   return False
#    elif c.lower().startswith("play"):
#        song=c.lower().split(" ")[1]
#        link= musicLibrary.music[song]
#        webbrowser.open(link)

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
           
            