import requests
import json

from datetime import datetime

# cuddles47's openweathermap api , pls sign in and use your, it's free
api_key = "52c343b2cd2594fee36890a128b43a4d"
base_url = "https://api.openweathermap.org/data/2.5/weather?"

def get_weather_data(city_name):
    url = f"{base_url}q={city_name}&appid={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = json.loads(response.text)

        # Handle missing sunrise timestamp
        if "sunrise" not in weather_data["sys"]:
            weather_data["sys"]["sunrise"] = None

        # Convert sunrise timestamp to integer if available
        if weather_data["sys"].get("sunrise"):
            weather_data["sys"]["sunrise"] = int(weather_data["sys"]["sunrise"])

        return weather_data
    else:
        print(f"Error fetching weather data for {city_name}: {response.status_code}")
        return None

def sky_condition(weather_data,humidity,temp,wind,clouds):
  if humidity in range(40,60) and temp in range(15,25):
    if wind < 15 and clouds < 10:
      return "Cotton candy clouds have vanished, leaving behind a canvas of pure, unblemished blue." # clear blue sky
    elif wind < 15 and clouds < 60:
      return "Nice and bright, with a few clouds." if clouds < 30 else "Not all sunshine, but still bright." # mostly sunny and partly cloudy
    else:
      return "Windy day. Leaves flying, clouds scooting." if wind >= 15 else "Cloudy today. Sky's in a gray mood." # windy and cloudy
  else:
    if humidity >= 60:
      return "The world seems to sweat under the oppressive weight of the humidity." # humid
    elif temp <= 15:
      return "Cold enought to make a polar bear shiver."                     # cold
    elif temp >= 25:
      return "Today temperature remind me of how hot Andy Blossom is."       # hot
    else:
      return "It's hard to say what the weather will be like cause mother Nature's playing roulette with the weather today.\n You should dress for every season, just in case xD. "

def weather_report(weather_data):
    # Extract weather information
    description = weather_data["weather"][0]["description"]
    temp = round(weather_data["main"]["temp"] - 273.15, 2)
    humidity = weather_data["main"]["humidity"] 
    wind = weather_data["wind"]["speed"]
    clouds = weather_data["clouds"]["all"]
    if isinstance(weather_data["sys"]["sunrise"], int):
        sunrise_time = datetime.fromtimestamp(weather_data["sys"]["sunrise"]).strftime("%H:%M")
    else:
        sunrise_time = "N/A"
    if isinstance(weather_data["sys"]["sunset"],int):
        sunset_time = datetime.fromtimestamp(weather_data["sys"]["sunset"]).strftime("%H:%M")
    else:
        sunset_time = "N/A"

    # Build the report with conditional logic
    report = f"It is currently {description} and {temp}°C in {city_name}.\n"
    report += f"Humidity: {humidity}%.\n"
    report += f"Wind: Speed {weather_data['wind']['speed']} m/s, direction {weather_data['wind']['deg']} degrees.\n"
    report += f"Clouds: {weather_data['clouds']['all']}%.\n"
    report += f"The official sunrise time in {city_name} is {sunrise_time}. Sunset is expected at {sunset_time}.\n"  
    report += f"{sky_condition(weather_data,humidity,temp,wind,clouds)}."
    return report


# Prompt user for city name
city_name = input("Enter the city you'd like the weather report for: ")

# Get weather data and format report
weather_data = get_weather_data(city_name)
if weather_data:
    print(weather_report(weather_data))
else:
    print("Sorry, I couldn't find weather data for that city.")
