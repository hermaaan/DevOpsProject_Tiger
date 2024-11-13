import os
import sys
import requests
from dotenv import load_dotenv
from app import LAT, LON  

load_dotenv()

def test_weather_api():    
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API key is missing in the .env file")

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={api_key}&units=metric&lang=en"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        print("Integration test passed: Received OK status from OpenWeather API")
    else:
        print(f"Integration test failed: Received {response.status_code} from OpenWeather API")
        sys.exit(1)

if __name__ == '__main__':
    test_weather_api()
