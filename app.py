from flask import Flask, render_template, jsonify
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

#Coordinates
LAT = 59.3293  
LON = 18.0686  

@app.route('/')
def home():
    api_key = os.getenv('API_KEY') 
    if not api_key:
        return "API key is missing or incorrect in .env file"
    
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={api_key}&units=metric&lang=en"

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
    
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={api_key}&units=metric&lang=en"

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
