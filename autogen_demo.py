# -*- coding: utf-8 -*-

import autogen
import requests

API_KEY = "41c68af14e3fa28c5831c12347e6f86c"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather():
    params = {"q": "London", "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        return f"Weather in London: {weather}, Temperature: {temperature}°C"
    else:
        return "Sorry, I couldn't fetch the weather for London."

class WeatherAgent(autogen.AssistantAgent):
    def __init__(self, name="WeatherBot"):
        super().__init__(name=name)

    def process_message(self, message, sender):
        if "weather" in message.lower() and "london" in message.lower():
            return get_weather()
        return "I can only provide weather updates for London."

class UserAgent(autogen.UserProxyAgent):
    def __init__(self, name="User"):
        super().__init__(name=name)

    def send_message(self, message, receiver):
        print(f"\nUser: {message}")
        response = receiver.process_message(message, self)
        print(f"\n{receiver.name}: {response}\n")

if __name__ == "__main__":
    user = UserAgent()
    bot = WeatherAgent()

    user.send_message("What is the weather in London?", bot)

