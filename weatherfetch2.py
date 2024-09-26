import requests
import datetime


def get_weather_data(api_key, location, start_time, end_time):
    """
    Fetches weather data from OpenWeatherMap API for a given location and time range.
    """
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "appid": api_key,
        "q": location,
        "units": "metric"  # Get temperature in Celsius
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise exception for non-200 status codes
        data = response.json()

        # Debugging: print the entire response to understand the structure
        print("Full API Response:\n", data)

        # Filter data for the specified time range
        filtered_data = [
            forecast
            for forecast in data["list"]
            if datetime.datetime.strptime(forecast["dt_txt"], "%Y-%m-%d %H:%M:%S") >= datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            and datetime.datetime.strptime(forecast["dt_txt"], "%Y-%m-%d %H:%M:%S") <= datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        ]

        return filtered_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data from OpenWeatherMap: {e}")
        return []


def process_weather_data(weather_data):
    """
    Processes weather data and provides clothing recommendations.
    """
    recommendations = []
    for forecast in weather_data:
        # Extract temperature in Celsius
        temperature_celsius = forecast["main"]["temp"]

        # Debugging: print the temperature for each forecast
        print(f"Temperature at {forecast['dt_txt']}: {temperature_celsius}°C")

        # Iterate through weather conditions
        for weather in forecast["weather"]:
            weather_id = weather["id"]
            weather_description = weather["description"]

            # Debugging: print the weather condition for each forecast
            print(f"Weather condition at {forecast['dt_txt']}: {weather_description} (ID: {weather_id})")

            # Check for storm or rain conditions
            if weather_id in [200, 201, 202, 210, 211, 212, 221, 230, 231, 232]:
                recommendations.append("Bring a coat or umbrella!")

        # Check for cold temperatures
        if temperature_celsius < 10:
            recommendations.append("Bring a jumper!")

    # Return recommendations or a default message
    return ", ".join(recommendations) or "No specific clothing recommendations needed."


api_key = ""

location = "Bristol, UK"

# Specify start and end times
start_time = "2024-09-26 17:00:00"
end_time = "2024-09-27 03:00:00"

# Get weather data for the specified time range
weather_data = get_weather_data(api_key, location, start_time, end_time)

# Process weather data and get clothing recommendations
clothing_recommendations = process_weather_data(weather_data)

# Display the retrieved weather data and recommendations
print("\nWeather data from OpenWeatherMap:")
for forecast in weather_data:
    print(f"Date/Time: {forecast['dt_txt']}")
    print(f"Temperature: {forecast['main']['temp']}°C")
    print(f"Weather: {forecast['weather'][0]['description']}")

print("\nClothing Recommendations:")
print(clothing_recommendations)