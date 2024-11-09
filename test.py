import unittest
from app import app
from datetime import datetime

class TestWeatherAppDataTypes(unittest.TestCase):

    def setUp(self):
        # Set up the test client for the Flask app
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_update_weather_data_types(self):
        # Test the /update_weather route
        response = self.client.get('/update_weather')
        json_data = response.get_json()

        if response.status_code == 200:
            # Verify the data types of each field in the JSON response
            self.assertIsInstance(json_data['location'], str)
            self.assertIsInstance(json_data['temperature'], (int, float))
            self.assertIsInstance(json_data['description'], str)
            self.assertIsInstance(json_data['humidity'], int)
            self.assertIsInstance(json_data['wind_speed'], (int, float))

            # Check that sunrise and sunset are in string time format (HH:MM:SS)
            self.assertIsInstance(json_data['sunrise'], str)
            self.assertIsInstance(json_data['sunset'], str)
            try:
                datetime.strptime(json_data['sunrise'], '%H:%M:%S')
                datetime.strptime(json_data['sunset'], '%H:%M:%S')
            except ValueError:
                self.fail("Sunrise and sunset should be in HH:MM:SS format")
        else:
            # If API fails, verify error response format
            self.assertEqual(response.status_code, 500)
            self.assertIn('error', json_data)
            self.assertIsInstance(json_data['error'], str)

if __name__ == '__main__':
    unittest.main()
