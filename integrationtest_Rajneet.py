import os
import requests
from app import LAT, LON
from dotenv import load_dotenv

load_dotenv()

def test_weather_api():# Test the OpenWeather API and verify essential fields in the response."""
    
    # Load the API key from environment variables
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API key is missing in the .env file")

    # Construct the API URL using coordinates from app.py
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={api_key}&units=metric&lang=en"
    
    # Send GET request to OpenWeather API
    response = requests.get(url)

    # Check the response status code
    if response.status_code == 200:
        print("Integration test passed: Received OK status from OpenWeather API")

        # Verify that expected fields are present in the JSON response
        json_data = response.json()
        required_fields = ['name', 'main', 'weather', 'wind', 'sys']
        
        for field in required_fields:
            if field not in json_data:
                print(f"Integration test failed: Missing '{field}' field in API response")
                return
        
        print("Integration test passed: All required fields present in API response")

    else:
        print(f"Integration test failed: Received {response.status_code} from OpenWeather API")

if __name__ == '__main__':
    test_weather_api()
