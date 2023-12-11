import datetime
import json
import requests

# OpenWeatherMap API key
API_KEY = "e4dc53ac469bb81befdae7bda946d3e4"

# Fixed coordinates for Calicut
LATITUDE = 11.2588
LONGITUDE = 75.7804

# URL for OpenWeatherMap 3-Hour Forecast API
API_URL = "https://api.openweathermap.org/data/2.5/forecast"


def main():
    try:
        # Get user input for specific time
        input_time = input("Enter a specific time (format: YYYY-MM-DD HH:MM:SS): ")

        # Try parsing the input as a timestamp first
        try:
            user_time = datetime.datetime.strptime(input_time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            # If parsing as timestamp fails, try parsing as HH:MM
            try:
                user_time = datetime.datetime.strptime(input_time, "%H:%M")
            except ValueError:
                print("Invalid time format. Please enter a valid YYYY-MM-DD HH:MM:SS or HH:MM format.")
                return

        # Build the API request URL with parameters
        url = f"{API_URL}?lat={LATITUDE}&lon={LONGITUDE}&appid={API_KEY}"

        # Fetch weather data from OpenWeatherMap API
        response = requests.get(url)
        response.raise_for_status()

        # Parse JSON response
        data = json.loads(response.text)

        # Find closest forecast time to user input
        closest_forecast_time = None
        closest_time_diff = None
        for forecast in data["list"]:
            forecast_time = datetime.datetime.fromtimestamp(forecast["dt"])
            time_diff = abs(user_time - forecast_time)
            if closest_forecast_time is None or time_diff < closest_time_diff:
                closest_forecast_time = forecast_time
                closest_time_diff = time_diff

        # Extract weather information for closest forecast time
        # After extracting weather information
        if closest_forecast_time:
            weather_data = forecast
            print(f"Weather data for closest time ({closest_forecast_time}):")
            # convert kelvin to celcius
            celsius_temperature = weather_data['main']['temp'] - 273.15
            print(f"Temperature: {celsius_temperature:.2f}°C")
            print(f"Weather condition: {weather_data['weather'][0]['main']}")
            print(f"Humidity: {weather_data['main']['humidity']}%")
        else:
            print("Error: Could not find weather forecast for the specified time.")

    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    main()
