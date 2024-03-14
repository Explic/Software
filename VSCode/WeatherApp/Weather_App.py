# import and setting variables
import cutie
import os
from colorama import *
import requests
from datetime import datetime
class WeatherApp:
    def __init__(self):
        self.weather_locations = []
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

    # Clears the console and resets the text style
    def clear(self):
        if self.is_debug_mode == False:
            os.system('cls') 
        print(Style.RESET_ALL)
        
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
            print(answer)
        return answer

    # Function to get weather data from OpenWeather API
    def get_weather(self, location):
        api_key = "c9cf80040d93269dd66b49bf6e8a9196"
        if self.is_celcius == True:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
        else:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=imperial"
        response = requests.get(url)
        data = response.json()
        if self.is_debug_mode == True:
            print(data)
        return data

    # Function to add a location
    def inputLocation(self):
        loop = True
        while loop == True:
            location = input('Add a location or type back: ')
            location = location.capitalize()
            if location == 'Back':
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
                        input('Location ' + location + ' added, press enter to continue\n')
                        loop = False
                else:
                    self.clear()
                    print(Fore.LIGHTRED_EX + 'Failed to find location please try again' + Style.RESET_ALL)
            except Exception as e: # <--- Catch any errors
                self.clear()
                if self.is_debug_mode == True:
                    print(e)
                print(Fore.LIGHTRED_EX + 'An error has occurred' + Style.RESET_ALL)
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
        
    # Colours the Title cus its fun      
    def menu_colour(self):
        setting = self.menu('Colours', [Fore.LIGHTRED_EX + 'Red', Fore.BLUE + 'Blue', Fore.LIGHTCYAN_EX + 'Cyan', Fore.LIGHTMAGENTA_EX + 'Pink', Fore.LIGHTWHITE_EX + 'White'])
        if setting == Fore.LIGHTRED_EX + 'Red':
            self.colour = Fore.LIGHTRED_EX
        elif setting == Fore.BLUE + 'Blue':
            self.colour = Fore.BLUE
        elif setting == Fore.LIGHTCYAN_EX + 'Cyan':
            self.colour = Fore.LIGHTCYAN_EX
        elif setting == Fore.LIGHTMAGENTA_EX + 'Pink':
            self.colour = Fore.LIGHTMAGENTA_EX
        elif setting == Fore.LIGHTWHITE_EX + 'White':
            self.colour = Fore.LIGHTWHITE_EX

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
        data = self.get_weather(location)
        if data['cod'] == 200:
            self.clear()
            if self.is_celcius == True:
                x = '°C'
            else:
                x = '°F'
            
            # adds Failed to find data if it fails to find the data
            try:
                self.print_summary(data),
            except:
                print('Weather in ' + Fore.LIGHTRED_EX + 'Failed to find data' + Style.RESET_ALL)
            try:
                self.print_coordinates(data),
            except:
                print('Coordinates: ' + Fore.LIGHTRED_EX + 'Failed to find data' + Style.RESET_ALL)
            try:   
                self.print_weather(data),
            except:
                print('Weather: ' + Fore.LIGHTRED_EX + 'Failed to find data' + Style.RESET_ALL)
            try:
                self.print_temperature(data, x),
            except:
                print('Temperature: ' + Fore.LIGHTRED_EX + 'Failed to find data' + Style.RESET_ALL)
            try:
                self.print_temperature_extra(data, x),
            except:
                print('Feels like : ' + Fore.LIGHTRED_EX + 'Failed to find data' + Style.RESET_ALL)
                print('Max Temp: ' + Fore.LIGHTRED_EX + 'Failed to find data' + Style.RESET_ALL)
                print('Min Temp: ' + Fore.LIGHTRED_EX + 'Failed to find data' + Style.RESET_ALL) 
            try:
                self.print_humidity(data),
            except:
                print('Humidity: ' + Fore.LIGHTRED_EX + 'Failed to find data' + Style.RESET_ALL)
            try:
                self.print_atmospheric_pressure(data),
            except:
                print('Sea Level: ' + Fore.LIGHTRED_EX + 'Failed to find data' + Style.RESET_ALL)
                print('Ground Level: ' + Fore.LIGHTRED_EX + 'Failed to find data' + Style.RESET_ALL)
            try:
                self.print_wind(data),
            except:
                print('Wind: ' + Fore.LIGHTRED_EX + 'Failed to find data' + Style.RESET_ALL)
            try:
                self.print_cloud_percentage(data),
            except: 
                print('Cloud Percentage: ' + Fore.LIGHTRED_EX + 'Failed to find data' + Style.RESET_ALL)
            try:
                self.print_sunrise_sunset(data)
            except:
                print('Sunrise: ' + Fore.LIGHTRED_EX + 'Failed to find data' + Style.RESET_ALL)
                print('Sunset: ' + Fore.LIGHTRED_EX + 'Failed to find data' + Style.RESET_ALL)
                     
            input('Press enter to continue\n')

    # Print Summary
    def print_summary(self, data):
        location = data['name']
        if self.show_country:
            location += f", {data['sys']['country']}"
        print(Style.BRIGHT + Fore.LIGHTWHITE_EX + f"Weather in {location}:\n" + Style.RESET_ALL)

    # Print Coordinates
    def print_coordinates(self, data):
                if self.show_coord:
                    print(f"Coordinates: {data['coord']['lon']}, {data['coord']['lat']}")

    # Print Weather
    def print_weather(self, data):
        if self.show_weather:
            print(f"Weather: {data['weather'][0]['main']} ({data['weather'][0]['description']})".capitalize())

    # Print Temperature
    def print_temperature(self, data, x):
        if self.show_temp:
            print(f"Temperature: {data['main']['temp']} {x}")

    # Print Extra Temperature Information
    def print_temperature_extra(self, data, x):
        if self.show_temp_extra:
            print(f"Feels like: {data['main']['feels_like']} {x}")
            print(f"Max Temp: {data['main']['temp_max']} {x}")
            print(f"Min Temp: {data['main']['temp_min']} {x}")

    # Print Humidity
    def print_humidity(self, data):
        if self.show_humidity:
            print(f"Humidity: {data['main']['humidity']}%")
            
    # Print Atmospheric Pressure
    def print_atmospheric_pressure(self, data):
        if self.show_atmospheric_pressure:
            print(f"Atmospheric Pressure: {data['main']['pressure']} hPa")
            print(f"Sea Level: {data['main']['sea_level']} hPa")
            print(f"Ground Level: {data['main']['grnd_level']} hPa")

    # Print Wind
    def print_wind(self, data):
        if self.show_wind:
            print(f"Wind: {data['wind']['speed']} m/s")

    # Print Cloud Percentage
    def print_cloud_percentage(self, data):
        if self.show_cloud_percent:
            print(f"Cloud Percentage: {data['clouds']['all']}%")

    # Print Sunrise and Sunset
    def print_sunrise_sunset(self, data):
        if self.show_sunrise_sunset:
            print(f"Sunrise: {datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S')}")
            print(f"Sunset: {datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S')}") 

    # decides if the user has inputted a location or not and then runs the function to get the weather data
    def menu_get_weather(self):
        if self.weather_locations == []:
            print (Fore.LIGHTRED_EX + 'No locations saved, please add a location' + Style.RESET_ALL)
            input('Press enter to continue\n')
            return
        else:
            selection = self.menu('Pick a saved location:', self.weather_locations + [Fore.LIGHTRED_EX + 'Back'])
            self.PWeather(selection)

    # Menu to pick a location
    def menu_pick_location(self):
        loop = True
        while loop == True:
            if self.weather_locations == []: # <--- Check if there are any locations saved, if not it goes straight to asking for a location
                x = self.inputLocation()
                if x == False:
                    loop = False
                    break
            #
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

        return

    # main menu
    # selections: Get Weather, Saved Locations, Settings, Exit
    def menu_home(self):
        loop = True
        self.is_debug_mode = False
        while loop == True:
            choice = self.menu('Weather App', ['Get Weather', 'Saved Locations', 'Settings', Fore.LIGHTRED_EX + 'Exit'])
            
            if choice == 'Get Weather':
                self.menu_get_weather()
                
            elif choice == 'Saved Locations':
                self.menu_pick_location()
                
            elif choice == 'Settings':
                self.menu_settings()
                
            elif choice == Fore.LIGHTRED_EX + 'Exit':
                print(Style.RESET_ALL + 'Goodbye!')
                exit()

# Run the weather app
try:
    app = WeatherApp()
    app.menu_home()
except KeyboardInterrupt:
    print(Style.RESET_ALL + 'Goodbye!')
    exit()

    
