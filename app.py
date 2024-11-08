from flask import Flask, render_template, jsonify
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check route"""
    return "Healthy", 200

@app.route('/')
def home():
    api_key = os.getenv('API_KEY') 
    if not api_key:
        return "API key is missing or incorrect in .env file"
    
    lat = 59.3293
    lon = 18.0686
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=en"

    response = requests.get(url)
    if response.status_code == 200:
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
        return render_template('weather.html', weather=weather_data)
    else:
        return f"Error: {response.status_code}"

@app.route('/update_weather', methods=['GET'])
def update_weather():
    api_key = os.getenv('API_KEY')
    if not api_key:
        return jsonify({"error": "API key is missing or incorrect in .env file"}), 400
    
    lat = 59.3293
    lon = 18.0686
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=en"

    response = requests.get(url)
    if response.status_code == 200:
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
        return jsonify(weather_data)
    else:
        return jsonify({"error": "Failed to fetch weather data"}), 500

if __name__ == '__main__':
    app.run(debug=True)
