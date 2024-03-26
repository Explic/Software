# import and setting variables
# Cutie is used to make the menus
import cutie
# os is used to clear the console
import os
# colorama is used to change the text colour, e.g. Fore.LIGHTRED_EX
from colorama import *
# requests is used to get the weather data from the OpenWeather API
import requests
# datetime is used to convert the sunrise and sunset times from Unix time to a readable format
from datetime import datetime
# used to save the settings to a file
import json

import time


# Define the WeatherApp class
class WeatherApp:
    # Initialises the class and sets the default values for the settings
    def __init__(self):
        self.load_locations() # <--- Load the locations from a file
        self.load_settings() # <--- Load the settings from a file
        

    # Clears the console and resets the text style
    def clear(self):
        if self.is_debug_mode == False:
            os.system('cls') 
        print(Style.RESET_ALL)
    
    # Loads the settings from a file 
    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                self.is_celcius = settings['is_celcius']
                self.is_debug_mode = settings['is_debug_mode']
                self.colour = settings['colour']
                self.show_coord = settings['show_coord']
                self.show_weather = settings['show_weather']
                self.show_country = settings['show_country']
                self.show_temp = settings['show_temp']
                self.show_temp_extra = settings['show_temp_extra']
                self.show_humidity = settings['show_humidity']
                self.show_atmospheric_pressure = settings['show_atmospheric_pressure']
                self.show_wind = settings['show_wind']
                self.show_cloud_percent = settings['show_cloud_percent']
                self.show_sunrise_sunset = settings['show_sunrise_sunset']
        except:
            self.is_celcius = True
            self.is_debug_mode = False
            self.colour = Fore.LIGHTWHITE_EX
            self.show_coord = False
            self.show_weather = True
            self.show_country = False
            self.show_temp = True
            self.show_temp_extra = False
            self.show_humidity = False
            self.show_atmospheric_pressure = False
            self.show_wind = False
            self.show_cloud_percent = False
            self.show_sunrise_sunset = False
    
    # Saves the settings to a file  
    def save_settings(self):
        try: 
            settings = {
                'is_celcius': self.is_celcius,
                'is_debug_mode': self.is_debug_mode,
                'colour': self.colour,
                'show_coord': self.show_coord,
                'show_weather': self.show_weather,
                'show_country': self.show_country,
                'show_temp': self.show_temp,
                'show_temp_extra': self.show_temp_extra,
                'show_humidity': self.show_humidity,
                'show_atmospheric_pressure': self.show_atmospheric_pressure,
                'show_wind': self.show_wind,
                'show_cloud_percent': self.show_cloud_percent,
                'show_sunrise_sunset': self.show_sunrise_sunset
            }
            with open('settings.json', 'w') as f:
                json.dump(settings, f)
        except:
            print(Fore.LIGHTRED_EX + 'Failed to save settings' + Style.RESET_ALL)
        
    # Saves the locations to a file
    def save_locations(self):
        try:
            with open('locations.json', 'w') as f:
                json.dump(self.weather_locations, f)
        except:
            print(Fore.LIGHTRED_EX + 'Failed to save locations' + Style.RESET_ALL)
    
    # Loads the locations from a file
    def load_locations(self):
        try:
           with open('locations.json', 'r') as f:
                self.weather_locations = json.load(f)
        except:
            self.weather_locations = []
        
    def write_log(self, message):
        try:
            log = f'{datetime.now().strftime("%H:%M:%S")},  {message}\n'
            with open('logs.txt', 'a') as f:
                f.write(log)
        except:
            print(Fore.LIGHTRED_EX + 'Failed to write to logs' + Style.RESET_ALL)
    
    # Function to make menus easier to use, and colour them
    # Example: self.menu('Weather App', ['White', Fore.MAGENTA + 'Magenta', Fore.BLUE + 'Blue', Fore.GREEN + 'Green', Fore.RED + 'Red'])
    def menu(self, title, options):
        self.clear()
        if title != str('none'):
            print(self.colour + Style.BRIGHT + title + '\n')
        answer = options[cutie.select(
            options,
            deselected_prefix= Style.RESET_ALL + Style.DIM + '',
            selected_prefix= Style.RESET_ALL + ' ',
            caption_prefix= Fore.CYAN + '',
            )]
    
        self.clear()
        if self.is_debug_mode == True:
            print(Fore.LIGHTGREEN_EX + 'Selected: ' + Style.RESET_ALL + answer)
        return answer

    # Function to get weather data from OpenWeather API
    def get_weather(self, location):
        # My api key
        api_key = "c9cf80040d93269dd66b49bf6e8a9196"

        if self.is_celcius == True:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
        else:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=imperial"
        response = requests.get(url)
        data = response.json()
        if self.is_debug_mode == True:
            print(data)
            self.write_log('GET_WEATHER_DATA: ' + str(data))
        return data

    def get_forecast(self, location):
        api_key = "c9cf80040d93269dd66b49bf6e8a9196"
        if self.is_celcius == True:
            url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units=metric"
        else:
            url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units=imperial"
        response = requests.get(url)
        data = response.json()
        if self.is_debug_mode == True:
            print(data)
            self.write_log('GET_FORECAST_DATA: ' + str(data))
        return data
    
    # Function to add a location
    def inputLocation(self):
        loop = True
        while loop == True:
            location = input('Add a location or type back: ')
            location = location.capitalize()
            if location == 'Back' or location == '':
                loop = False
                break
            
            try:
                data = self.get_weather(location)                    
                if data['cod'] == 200:
                    if location in self.weather_locations: # <--- Check if location is already in list
                        self.clear()
                        print(Fore.LIGHTRED_EX + 'Location already added' + Style.RESET_ALL)
                        
                    else:
                        self.weather_locations.append(location) # <--- Add location to list
                        self.save_locations() # <--- Save the locations to a file
                        self.write_log('Location ' + location + ' added')
                        input('Location ' + location + ' added, press enter to continue\n')
                        loop = False
                else:
                    self.clear()
                    print(Fore.LIGHTRED_EX + 'Failed to find location please try again' + Style.RESET_ALL)
            except Exception as e: # <--- Catch any errors
                self.clear()
                if self.is_debug_mode == True:
                    self.write_log('Failed to find location: ' + location)
                    print(e)
                print(Fore.LIGHTRED_EX + 'An error has occurred' + Style.RESET_ALL)
                self.write_log('Failed to find location: ' + location)
        if self.weather_locations == []:
            return False
        else:
            return True
        
    # Function to remove a location        
    def removeLocation(self):
        loop = True
        while loop == True:
            if self.weather_locations == []:
                print(Fore.LIGHTRED_EX + 'No locations to remove' + Style.RESET_ALL)
                loop = False
                break
            else:
                selection = self.menu('Remove a Location:', self.weather_locations + [Fore.LIGHTRED_EX + 'Back'])
                if selection == Fore.LIGHTRED_EX + 'Back':
                    loop = False
                    break
                else:
                    self.weather_locations.remove(selection)
                    self.save_locations()
                    self.write_log('Location ' + selection + ' removed')
                    print(Fore.LIGHTGREEN_EX + 'Location removed' + Style.RESET_ALL)
                    input('Press enter to continue\n')
        return
        
    # Allows the user to change what information is shown
    def menu_shown_information(self):
        settings = [
            ('Coordinates', 'show_coord'),
            ('Weather', 'show_weather'),
            ('Country', 'show_country'),
            ('Temperature', 'show_temp'),
            ('Extra Temp Info', 'show_temp_extra'),
            ('Humidity', 'show_humidity'),
            ('Atmospheric Pressure', 'show_atmospheric_pressure'),
            ('Wind', 'show_wind'),
            ('Cloud Percentage', 'show_cloud_percent'),
            ('Sunrise/Sunset', 'show_sunrise_sunset')
        ]

        while True:
            options = [Fore.LIGHTGREEN_EX + 'Turn All On']
            for name, attr in settings:
                indicator = Fore.LIGHTGREEN_EX + ' ON' if getattr(self, attr) else Fore.RED + ' OFF'
                options.append(name + indicator)
            options.append(Fore.LIGHTRED_EX + 'Back')

            setting = self.menu('Shown Information', options)

            if setting == Fore.LIGHTGREEN_EX + 'Turn All On':
                for _, attr in settings:
                    setattr(self, attr, True)
            elif setting == Fore.LIGHTRED_EX + 'Back':
                break
            else:
                for name, attr in settings:
                    if setting.startswith(name):
                        setattr(self, attr, not getattr(self, attr))
                        break
        
    # Function to allow the user to change the color of the title text   
    def menu_colour(self):
        setting = self.menu('Colours', [Fore.LIGHTRED_EX + 'Red', Fore.BLUE + 'Blue', Fore.LIGHTCYAN_EX + 'Cyan', Fore.LIGHTMAGENTA_EX + 'Pink', Fore.GREEN + 'Green', Fore.YELLOW + 'Yellow', Fore.LIGHTWHITE_EX + 'White'])
        if setting == Fore.LIGHTRED_EX + 'Red':
            self.colour = Fore.LIGHTRED_EX
        elif setting == Fore.BLUE + 'Blue':
            self.colour = Fore.BLUE
        elif setting == Fore.LIGHTCYAN_EX + 'Cyan':
            self.colour = Fore.LIGHTCYAN_EX
        elif setting == Fore.LIGHTMAGENTA_EX + 'Pink':
            self.colour = Fore.LIGHTMAGENTA_EX
        elif setting == Fore.GREEN + 'Green':
            self.colour = Fore.GREEN
        elif setting == Fore.LIGHTWHITE_EX + 'White':
            self.colour = Fore.LIGHTWHITE_EX
        elif setting == Fore.YELLOW + 'Yellow':
            self.colour = Fore.YELLOW

    # Example Data from OpenWeather API:
    # {'coord': {'lon': 151.15, 'lat': -33.6333}, 
    # 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}],
    # 'base': 'stations',
    # 'main': {'temp': 27.65, 'feels_like': 28.15, 'temp_min': 24.65, 'temp_max': 29.75, 'pressure': 1013, 'humidity': 51, 'sea_level': 1013, 'grnd_level': 993},
    # 'visibility': 10000, 
    # 'wind': {'speed': 3.97, 'deg': 75, 'gust': 3.58}, 
    # 'clouds': {'all': 97}, 
    # 'dt': 1710305980, 
    # 'sys': {'type': 2, 'id': 2008671, 'country': 'AU', 'sunrise': 1710273193, 'sunset': 1710317805}, 
    # 'timezone': 39600, 'id': 2176081, 'name': 'Berowra', 'cod': 200}

    # Print the weather data, format it, and handle errors
    def PWeather(self, location):
        self.write_log('USER_GET_WEATHER ' + location)
        data = self.get_weather(location)
        if data['cod'] == 200:
            self.clear()
            if self.is_celcius == True:
                x = '°C'
            else:
                x = '°F'
            
            # Print each type of weather information, if available
            try:
                self.print_summary(data),
            except:
                print('Weather in ' + Fore.LIGHTRED_EX + 'Failed to find data' + Style.RESET_ALL)
                self.write_log('Weather in: '  'Failed to find data')
            try:
                self.print_coordinates(data),
            except:
                print('Coordinates: ' + Fore.LIGHTRED_EX + 'Failed to find data' + Style.RESET_ALL)
                self.write_log('Coordinates: '  'Failed to find data')
            try:   
                self.print_weather(data),
            except:
                print('Weather: ' + Fore.LIGHTRED_EX + 'Failed to find data' + Style.RESET_ALL)
                self.write_log('Weather: '  'Failed to find data')
            try:
                self.print_temperature(data, x),
            except:
                print('Temperature: ' + Fore.LIGHTRED_EX + 'Failed to find data' + Style.RESET_ALL)
                self.write_log('Temperature: '  'Failed to find data')
            try:
                self.print_temperature_extra(data, x),
            except:
                print('Feels like : ' + Fore.LIGHTRED_EX + 'Failed to find data' + Style.RESET_ALL)
                print('Max Temp: ' + Fore.LIGHTRED_EX + 'Failed to find data' + Style.RESET_ALL)
                print('Min Temp: ' + Fore.LIGHTRED_EX + 'Failed to find data' + Style.RESET_ALL) 
                self.write_log('Feels like: '  'Failed to find data')
                self.write_log('Max Temp: '  'Failed to find data')
                self.write_log('Min Temp: '  'Failed to find data')
            try:
                self.print_humidity(data),
            except:
                print('Humidity: ' + Fore.LIGHTRED_EX + 'Failed to find data' + Style.RESET_ALL)
                self.write_log('Humidity: '  'Failed to find data')
            try:
                self.print_atmospheric_pressure(data),
            except:
                print('Sea Level: ' + Fore.LIGHTRED_EX + 'Failed to find data' + Style.RESET_ALL)
                print('Ground Level: ' + Fore.LIGHTRED_EX + 'Failed to find data' + Style.RESET_ALL)
                self.write_log('Sea Level: '  'Failed to find data')
                self.write_log('Ground Level: '  'Failed to find data')
            try:
                self.print_wind(data),
            except:
                print('Wind: ' + Fore.LIGHTRED_EX + 'Failed to find data' + Style.RESET_ALL)
                self.write_log('Wind: '  'Failed to find data')
            try:
                self.print_cloud_percentage(data),
            except: 
                print('Cloud Percentage: ' + Fore.LIGHTRED_EX + 'Failed to find data' + Style.RESET_ALL)
                self.write_log('Cloud Percentage: '  'Failed to find data')
            try:
                self.print_sunrise_sunset(data)
            except:
                print('Sunrise: ' + Fore.LIGHTRED_EX + 'Failed to find data' + Style.RESET_ALL)
                print('Sunset: ' + Fore.LIGHTRED_EX + 'Failed to find data' + Style.RESET_ALL)
                self.write_log('Sunrise: '  'Failed to find data')
                self.write_log('Sunset: '  'Failed to find data')
                     
            input('\nPress enter to continue\n')

    # Print Summary
    def print_summary(self, data):
        location = data['name']
        if self.show_country:
            location += f", {data['sys']['country']}"
        print(Style.BRIGHT + Fore.LIGHTWHITE_EX + f"Weather in {location}:\n" + Style.RESET_ALL)
        self.write_log('Weather in: ' + location)

    # Print Coordinates
    def print_coordinates(self, data):
                if self.show_coord:
                    print(f"Coordinates: {data['coord']['lon']}, {data['coord']['lat']}")
                    self.write_log('Coordinates: ' + str(data['coord']['lon']) + ', ' + str(data['coord']['lat']))

    # Print Weather
    def print_weather(self, data):
        if self.show_weather:
            print(f"Weather: {data['weather'][0]['main']} ({data['weather'][0]['description']})".capitalize())
            self.write_log('Weather: ' + data['weather'][0]['main'] + ' (' + data['weather'][0]['description'] + ')')

    # Print Temperature
    def print_temperature(self, data, x):
        if self.show_temp:
            print(f"Temperature: {data['main']['temp']} {x}")
            self.write_log('Temperature: ' + str(data['main']['temp']) + ' ' + x)

    # Print Extra Temperature Information
    def print_temperature_extra(self, data, x):
        if self.show_temp_extra:
            print(f"Feels like: {data['main']['feels_like']} {x}")
            print(f"Max Temp: {data['main']['temp_max']} {x}")
            print(f"Min Temp: {data['main']['temp_min']} {x}")
            self.write_log('Feels like: ' + str(data['main']['feels_like']) + ' ' + x)
            self.write_log('Max Temp: ' + str(data['main']['temp_max']) + ' ' + x)
            self.write_log('Min Temp: ' + str(data['main']['temp_min']) + ' ' + x)

    # Print Humidity
    def print_humidity(self, data):
        if self.show_humidity:
            print(f"Humidity: {data['main']['humidity']}%")
            self.write_log('Humidity: ' + str(data['main']['humidity']) + '%')
            
    # Print Atmospheric Pressure
    def print_atmospheric_pressure(self, data):
        if self.show_atmospheric_pressure:
            print(f"Atmospheric Pressure: {data['main']['pressure']} hPa")
            print(f"Sea Level: {data['main']['sea_level']} hPa")
            print(f"Ground Level: {data['main']['grnd_level']} hPa")
            self.write_log('Atmospheric Pressure: ' + str(data['main']['pressure']) + ' hPa')
            self.write_log('Sea Level: ' + str(data['main']['sea_level']) + ' hPa')
            self.write_log('Ground Level: ' + str(data['main']['grnd_level']) + ' hPa')
            

    # Print Wind
    def print_wind(self, data):
        if self.show_wind:
            print(f"Wind: {data['wind']['speed']} m/s") 
            self.write_log('Wind: ' + str(data['wind']['speed']) + ' m/s')

    # Print Cloud Percentage
    def print_cloud_percentage(self, data):
        if self.show_cloud_percent:
            print(f"Cloud Percentage: {data['clouds']['all']}%")
            self.write_log('Cloud Percentage: ' + str(data['clouds']['all']) + '%')

    # Print Sunrise and Sunset
    def print_sunrise_sunset(self, data):
        if self.show_sunrise_sunset:
            # Convert the sunrise and sunset times from Unix time to a readable format
            print(f"Sunrise: {datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M')}")
            print(f"Sunset: {datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')}") 
            self.write_log('Sunrise: ' + datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'))
            self.write_log('Sunset: ' + datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M'))

    # Print the forecast data, For the next 5 days at 3 hour intervals
    def print_forecast(self, data, i, x):
        print(Style.BRIGHT + f"{datetime.fromtimestamp(data['list'][i]['dt']).strftime('%H:%M')}  " + Style.RESET_ALL + f"{data['list'][i]['main']['temp']} {x} - {data['list'][i]['weather'][0]['main']}".capitalize())
        self.write_log(f"{datetime.fromtimestamp(data['list'][i]['dt']).strftime('%H:%M')}  {data['list'][i]['main']['temp']} {x} - {data['list'][i]['weather'][0]['main']}".capitalize())

    def PForecast(self, location):
        previous_day = ''
        data = self.get_forecast(location)
        if data['cod'] == '200':
            self.clear()
            if self.is_celcius == True:
                x = '°C'
            else:
                x = '°F'
            print(Style.BRIGHT + self.colour + f"Weather Forecast for {location}:" + Style.RESET_ALL)
            for i in range (0, 40):
                try:
                    time.sleep(0.001)
                    if previous_day != datetime.fromtimestamp(data['list'][i]['dt']).strftime('%B %d'):
                        previous_day = datetime.fromtimestamp(data['list'][i]['dt']).strftime('%B %d')
                        print(Style.BRIGHT + Fore.LIGHTWHITE_EX + '\n' + previous_day + Style.RESET_ALL)
                    self.print_forecast(data, i, x)
                except:
                    print(Fore.LIGHTRED_EX + 'Failed to find data' + Style.RESET_ALL)
            input('\nPress enter to continue\n')
        else:
            print(Fore.LIGHTRED_EX + 'Failed to find location' + Style.RESET_ALL)
            input('Press enter to continue\n')

    # decides if the user has inputted a location or not and then runs the function to get the weather data
    def menu_get_weather(self):
        if self.weather_locations == []:
            print (Fore.LIGHTRED_EX + 'No locations saved, please add a location' + Style.RESET_ALL)
            input('Press enter to continue\n')
            return
        else:
            selection = self.menu('', ['Current Weather', 'Forecast', Fore.LIGHTRED_EX + 'Back'])
            if selection == Fore.LIGHTRED_EX + 'Back':
                return
            selected_location = self.menu('Pick a saved location:', self.weather_locations)
            if selection == 'Current Weather':
                self.PWeather(selected_location)
            elif selection == 'Forecast':
                self.PForecast(selected_location)

    # Menu to pick a location
    def menu_pick_location(self):
        loop = True
        while loop == True:
            if self.weather_locations == []: # <--- Check if there are any locations saved, if not it goes straight to asking for a location
                x = self.inputLocation()
                if x == False:
                    loop = False
                    break
            # If there are locations saved, it opens the menu to add or remove locations
            else:
                selection = self.menu('Saved Locations', ['Add a Location', 'Remove a Location', Fore.LIGHTRED_EX + 'Back'])
            
                if selection == Fore.LIGHTRED_EX + 'Back':
                    loop = False
                    break
                if selection == 'Add a Location':
                    x = self.inputLocation()
                    if x == False:
                        loop = False
                        break
                if selection == 'Remove a Location':
                    self.removeLocation()
                        
    # Settings menu            
    def menu_settings(self):
        setting = ''
        
        # indicator for debug mode
        while setting != Fore.LIGHTRED_EX + 'Back':
            if self.is_debug_mode == True:
                DOn = Fore.LIGHTGREEN_EX + ' ON'
            else:
                DOn = Fore.RED + ' OFF'
            
            # indicator for temperature unit
            if self.is_celcius == True:
                T = Fore.LIGHTGREEN_EX + '°C' + Fore.LIGHTWHITE_EX + ' < ' + Fore.LIGHTRED_EX + '°F'
            else:
                T = Fore.LIGHTRED_EX + '°C' + Fore.LIGHTWHITE_EX + ' > ' + Fore.LIGHTGREEN_EX + '°F'
                
            setting = self.menu('Settings', ['Temperature in ' + T, 'Debug Mode ' + DOn, 'Set Colour', 'Shown Information', Fore.LIGHTRED_EX + 'Back'])
            
            # Changes the setting to the opposite of what it is when it is selected
            if setting == 'Debug Mode ' + DOn:
                if self.is_debug_mode == True:
                    self.is_debug_mode = False
                else:
                    self.is_debug_mode = True
            
            # Opens the colour menu
            if setting == 'Set Colour':
                self.menu_colour()
            
            # Opens the shown information menu
            if setting == 'Shown Information':
                self.menu_shown_information()
                
            # Changes the temperature unit to opposite
            if setting == 'Temperature in ' + T:
                if self.is_celcius == True:
                    self.is_celcius = False
                else:
                    self.is_celcius = True
        
        # Saves the settings to a file
        self.save_settings()
        self.write_log('SAVED_SETTINGS')
        
        return

    # Help menu, explains how to use the app
    def help(self):
        self.clear()
        print(Fore.LIGHTWHITE_EX + Style.BRIGHT + 'Weather App Help\n' + Style.RESET_ALL)
        print('This is a simple weather app that uses the OpenWeather API to get weather data for a location.\n')
        print('Press' + Fore.LIGHTCYAN_EX + ' Up' + Style.RESET_ALL + ' or ' + Fore.LIGHTCYAN_EX + 'Down' + Style.RESET_ALL + ' to scroll through the menu and ' + Fore.LIGHTCYAN_EX + 'Enter' + Style.RESET_ALL + ' to select an option.\n')
        print('The app has a main menu with the following options:')
        print(Fore.LIGHTCYAN_EX + 'Get Weather' + Style.RESET_ALL + ' - Get the weather and forecast for a location')
        print(Fore.LIGHTCYAN_EX + 'Saved Locations' + Style.RESET_ALL + ' - Add, remove, or view saved locations')
        print(Fore.LIGHTCYAN_EX + 'Settings' + Style.RESET_ALL + ' - Change the settings for the app')
        print('You can select ' + Fore.LIGHTRED_EX + 'Exit' + Style.RESET_ALL + ' or press ' + Fore.LIGHTRED_EX + 'Ctrl+C' + Style.RESET_ALL + ' to exit the app.\n')
        print('When you select ' + Fore.LIGHTCYAN_EX + 'Get Weather' + Style.RESET_ALL + ' you can choose to the the current weather or the weather forecast for a saved location.')
        print('When you select ' + Fore.LIGHTCYAN_EX + 'Saved Locations' + Style.RESET_ALL + ' you can add, remove, and view saved locations.')
        print('When you select ' + Fore.LIGHTCYAN_EX + 'Settings' + Style.RESET_ALL + ' you can change the temperature unit, turn on debug mode, change the colour of the text, and change what information is shown.\n')
        print('In the settings menu:')
        print('You can change the temperature unit to either Celsius or Fahrenheit.')
        print('You can turn on debug mode to see the data from the OpenWeather API as well as history')
        print('You can change the colour of the text.')
        print('You can change what information is shown when you get the weather for a location.\n')
        print('Logs are saved in a folder named logs.txt\n')
        
        input('Press enter to continue\n')

    # main menu
    # selections: Get Weather, Saved Locations, Settings, Help, Exit
    def menu_home(self):
        loop = True
        self.write_log('USER_START')
        self.is_debug_mode = False
        while loop == True:
            choice = self.menu('Weather App', ['Get Weather', 'Saved Locations', 'Settings', Fore.LIGHTCYAN_EX + 'Help', Fore.LIGHTRED_EX + 'Exit'])
            
            if choice == 'Get Weather':
                self.write_log('USER_SELECT_GETWEATHER')
                self.menu_get_weather()
                
            elif choice == 'Saved Locations':
                self.write_log('USER_SELECT_SAVEDLOCATIONS')
                self.menu_pick_location()
                
            elif choice == 'Settings':
                self.write_log('USER_SELECT_SETTINGS')
                self.menu_settings()
            
            elif choice == Fore.LIGHTCYAN_EX + 'Help':
                self.write_log('USER_SELECT_HELP')
                self.help()
                
            elif choice == Fore.LIGHTRED_EX + 'Exit':
                self.write_log('USER_SELECT_EXIT')
                print(Style.RESET_ALL + 'Goodbye!')
                self.write_log('USER_EXIT\n\n\n')
                exit()

# Run the weather app
try:
    app = WeatherApp()
    app.menu_home()
except KeyboardInterrupt: # <--- If they press Ctrl+C it will exit the app instead of showing an error
    print(Style.RESET_ALL + 'Goodbye!')
    exit()
    
except Exception as e: # <--- Catch any errors
    print(Style.RESET_ALL + 'An error has occurred')
    print(e)
    input('Press enter to continue\n')

    
