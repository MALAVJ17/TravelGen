import requests

def get_weather(location):
    # Replace with your WeatherAPI key and proper error handling
    API_KEY = "e1a377cb32a747a380941918251304"
    URL = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={location}"
    
    try:
        res = requests.get(URL).json()
        temp = res["current"]["temp_c"]
        condition = res["current"]["condition"]["text"]
        return f"{temp}°C, {condition}"
    except:
        return "Weather info not available"
