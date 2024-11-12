import unittest
from app import app
from datetime import datetime

class TestWeatherApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):# Set up a test client for the Flask app
        cls.client = app.test_client()
        app.config['TESTING'] = True


    def test_update_weather_success_response(self): # Test the structure and data types in a successful /update_weather response."""
        response = self.client.get('/update_weather')
        
        if response.status_code == 200: # If the response is successful, check the data format
            json_data = response.get_json()
            
            # Check if each field is present and has the correct type
            self.assertIn('location', json_data, "Missing 'location' in response")
            self.assertIsInstance(json_data['location'], str, "'location' should be a string")
            
            self.assertIn('temperature', json_data, "Missing 'temperature' in response")
            self.assertIsInstance(json_data['temperature'], (int, float), "'temperature' should be an integer or float")
            
            self.assertIn('description', json_data, "Missing 'description' in response")
            self.assertIsInstance(json_data['description'], str, "'description' should be a string")
            
            self.assertIn('humidity', json_data, "Missing 'humidity' in response")
            self.assertIsInstance(json_data['humidity'], int, "'humidity' should be an integer")
            
            self.assertIn('wind_speed', json_data, "Missing 'wind_speed' in response")
            self.assertIsInstance(json_data['wind_speed'], (int, float), "'wind_speed' should be an integer or float")
            
            self.assertIn('sunrise', json_data, "Missing 'sunrise' in response")
            self.assertIsInstance(json_data['sunrise'], str, "'sunrise' should be a string in 'HH:MM:SS' format")
            
            self.assertIn('sunset', json_data, "Missing 'sunset' in response")
            self.assertIsInstance(json_data['sunset'], str, "'sunset' should be a string in 'HH:MM:SS' format")
            
            # Check if sunrise and sunset strings are in HH:MM:SS format
            for time_field in ['sunrise', 'sunset']:
                try:
                    datetime.strptime(json_data[time_field], '%H:%M:%S')
                except ValueError:
                    self.fail(f"{time_field} should be in 'HH:MM:SS' format")
        
    def test_update_weather_error_response(self): # Test that the error message is returned correctly if the API fails."""
        response = self.client.get('/update_weather')
        
        # If the response status code indicates a failure, check for an error message
        if response.status_code == 500:
            json_data = response.get_json()
            self.assertIn('error', json_data, "Error message missing from response")
            self.assertIsInstance(json_data['error'], str, "'error' should be a string")

if __name__ == '__main__':
    unittest.main()
