import requests


def get_weather(city, speak):

    try:
        print(f"Fetching weather for: {city}")

        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        }

        response = requests.get(
            geo_url,
            params=geo_params,
            timeout=10
        )

        data = response.json()

        if "results" not in data:
            print(f"City not found: {city}")
            speak("Sorry, I could not find that city.")
            return

        latitude = data["results"][0]["latitude"]
        longitude = data["results"][0]["longitude"]
        city_name = data["results"][0]["name"]

        print(f"Found city: {city_name} ({latitude}, {longitude})")

        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,weather_code",
            "temperature_unit": "celsius"
        }

        response = requests.get(
            weather_url,
            params=weather_params,
            timeout=10
        )

        weather = response.json()["current"]

        temperature = weather["temperature_2m"]
        humidity = weather["relative_humidity_2m"]
        code = weather["weather_code"]

        conditions = {
            0: "clear sky",
            1: "mainly clear",
            2: "partly cloudy",
            3: "cloudy",
            45: "foggy",
            48: "foggy",
            51: "light rain",
            53: "rain",
            55: "heavy rain",
            61: "light rain",
            63: "rain",
            65: "heavy rain",
            80: "rain showers",
            81: "rain showers",
            82: "heavy rain showers",
            95: "thunderstorm"
        }

        condition = conditions.get(code, "normal weather")

        weather_text = (
            f"The weather in {city_name} is "
            f"{temperature} degrees Celsius with {condition}. "
            f"Humidity is {humidity} percent."
        )

        print(f"Weather Result: {weather_text}")
        speak(weather_text)

    except Exception as e:
        print(f"Weather Error: {e}")
        speak("Sorry, I could not get the weather.")