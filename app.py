from flask import Flask, render_template, jsonify
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

LAT = 59.3293
LON = 18.0686
API_KEY = os.getenv('API_KEY')
WEATHER_API_URL = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric&lang=en"

if not API_KEY:
    raise ValueError("API key is missing in .env file")

def fetch_weather_data():
    try:
        response = requests.get(WEATHER_API_URL)
        response.raise_for_status()  
        data = response.json()

        sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S')
        sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S')
        weather_data = {
            'location': data['name'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'sunrise': sunrise,
            'sunset': sunset
        }
        return weather_data
    except requests.RequestException as e:
        app.logger.error(f"Error fetching weather data: {e}")
        return None

@app.route('/')
def home():
    weather_data = fetch_weather_data()
    if weather_data:
        return render_template('weather.html', weather=weather_data)
    return "Error: Unable to fetch weather data", 500

@app.route('/update_weather', methods=['GET'])
def update_weather():
    weather_data = fetch_weather_data()
    if weather_data:
        return jsonify(weather_data)
    return jsonify({"error": "Failed to fetch weather data"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)