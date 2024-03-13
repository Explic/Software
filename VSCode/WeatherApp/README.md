# Weather App

This is a simple console-based weather application written in Python. It uses the OpenWeather API to fetch weather data for different locations.

## Features

- Get current weather data for any location
- Save locations for quick access
- Customize the information displayed (coordinates, temperature, humidity, etc.)
- Change the display colour
- Debug mode for troubleshooting and displaying past interactions
- Handle user errors and exceptions gracefully.

## Requirements

- Python 3
- `cutie` Python library
- `Colorama` Python library
- `requests` Python library

```bash
pip install cutie colorama requests
```

## How to use

1. Run the `Weather_App.py` script in your Python environment.
2. You will be presented with a menu with the following options: 'Get Weather', 'Saved Locations', 'Settings', 'Exit'.
3. Use UP and DOWN arrow keys to navigate the menu and use ENTER to select.
4. Before selecting 'Get Weather' you must Select 'Saved Locations' and add a location.
5. Select 'Get Weather' to fetch the weather data for your saved locations.
7. Select 'Settings' to customize the information displayed, change the display colour, or toggle the debug mode.
8. Select 'Exit' to close the application (You can also exit with ctrl+c).

## Settings

In the settings menu, you can:

- Switch between Celsius and Fahrenheit
- Turn on/off debug mode
- Change the colour of the menu
- Choose which weather information to display

## Customizable Information

You can customize the information displayed by the application. Here are the options:

- Coordinates: Display the geographical coordinates of the location
- Weather: Display the current weather condition (e.g., Cloudy, Sunny, etc.)
- Country: Display the country of the location
- Temperature: Display the current temperature
- Extra Temp Info: Display additional temperature information like "feels like", minimum and maximum temperature
- Humidity: Display the current humidity level
- Atmospheric Pressure: Display the current atmospheric pressure
- Wind: Display the wind speed
- Cloud Percentage: Display the percentage of cloud cover
- Sunrise/Sunset: Display the time of sunrise and sunset

You can toggle these options ON and OFF in the "Shown Information" section of the settings menu.

