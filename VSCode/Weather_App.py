# import and setting variables
import cutie
from cutie import *
import os
from colorama import *
import requests
from datetime import datetime
global celcius
global debug
global colour
global weatherLocations
weatherLocations = []
celcius = True
debug = False
colour = Fore.LIGHTWHITE_EX
global TCoord
global TWeather
global TCountry
global TTemp
global TTempExtra
global THumidity
global TAtmosphericPressure
global TWind
global TCloudPercent
global TSunriseSunset
TCoord = False
TWeather = True
TCountry = False
TTemp = True
TTempExtra = False
THumidity = False
TAtmosphericPressure = False
TWind = False
TCloudPercent = False
TSunriseSunset = False

#datetime.fromtimestamp(number).strftime('%d-%m-%y %H:%M:%S')

# Function to clear
def clear():
    global debug
    global colour
    if debug == False:
        os.system('cls')
    
    
    print(Style.RESET_ALL)
    
# Function to make menus easier to use, and colour them
# Example: menu('Weather App', ['White', Fore.MAGENTA + 'Magenta', Fore.BLUE + 'Blue', Fore.GREEN + 'Green', Fore.RED + 'Red'])
def menu(title, options):
    global debug
    global colour
    clear()
    if title != str('none'):
        print(colour + Style.BRIGHT + title + '\n')
    answer = options[cutie.select(
        options,
        deselected_prefix= Style.RESET_ALL + Style.DIM + '',
        selected_prefix= Style.RESET_ALL + ' ',
        caption_prefix= Fore.CYAN + '',
        )]
    
    clear()
    if debug == True:
        print(answer)
    return answer

# Function to get weather data from OpenWeather API
def get_weather(location):
    global celcius
    api_key = "c9cf80040d93269dd66b49bf6e8a9196"
    if celcius == True:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    else:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=imperial"
    response = requests.get(url)
    data = response.json()
    if debug == True:
        print(data)
    return data

def inputLocation():
    global weatherLocations
    loop = True
    while loop == True:
        location = input('Add a location or type back: ')
        location = location.capitalize()
        if location == 'Back':
            loop = False
            break
        
        try:
            data = get_weather(location)                    
            if data['cod'] == 200:
                if location in weatherLocations: # <--- Check if location is already in list
                    clear()
                    print(Fore.LIGHTRED_EX + 'Location already added' + Style.RESET_ALL)
                    
                else:
                    weatherLocations.append(location) # <--- Add location to list
                    input('Location ' + location + ' added, press enter to continue\n')
                    loop = False
            else:
                clear()
                print(Fore.LIGHTRED_EX + 'Failed to find location please try again' + Style.RESET_ALL)
        except Exception as e: # <--- Catch any errors
            clear()
            if debug == True:
                print(e)
            print(Fore.LIGHTRED_EX + 'An error has occurred' + Style.RESET_ALL)
    if weatherLocations == []:
        return False
    else:
        return True
    
            
def removeLocation():
    global weatherLocations
    loop = True
    while loop == True:
        if weatherLocations == []:
            print(Fore.LIGHTRED_EX + 'No locations to remove' + Style.RESET_ALL)
            loop = False
            break
        else:
            selection = menu('Remove a Location:', weatherLocations + [Fore.LIGHTRED_EX + 'Back'])
            if selection == Fore.LIGHTRED_EX + 'Back':
                loop = False
                break
            else:
                weatherLocations.remove(selection)
                print(Fore.LIGHTGREEN_EX + 'Location removed' + Style.RESET_ALL)
                input('Press enter to continue\n')
    return
    
# Allows the user to change what information is shown
def menu_shown_information():
    global debug
    global TCoord
    global TWeather
    global TCountry
    global TTemp
    global TTempExtra
    global THumidity
    global TAtmosphericPressure
    global TWind
    global TCloudPercent
    global TSunriseSunset
    loop = True
    while loop == True:
        T1 = Fore.LIGHTGREEN_EX + ' ON' if TCoord else Fore.RED + ' OFF'
        T2 = Fore.LIGHTGREEN_EX + ' ON' if TWeather else Fore.RED + ' OFF'
        T3 = Fore.LIGHTGREEN_EX + ' ON' if TCountry else Fore.RED + ' OFF'
        T4 = Fore.LIGHTGREEN_EX + ' ON' if TTemp else Fore.RED + ' OFF'
        T5 = Fore.LIGHTGREEN_EX + ' ON' if TTempExtra else Fore.RED + ' OFF'
        T6 = Fore.LIGHTGREEN_EX + ' ON' if THumidity else Fore.RED + ' OFF'
        T7 = Fore.LIGHTGREEN_EX + ' ON' if TAtmosphericPressure else Fore.RED + ' OFF'
        T8 = Fore.LIGHTGREEN_EX + ' ON' if TWind else Fore.RED + ' OFF'
        T9 = Fore.LIGHTGREEN_EX + ' ON' if TCloudPercent else Fore.RED + ' OFF'
        T10 = Fore.LIGHTGREEN_EX + ' ON' if TSunriseSunset else Fore.RED + ' OFF'
            
        setting = menu('Shown Information', ['Coordinates' + T1, 'Weather' + T2, 'Country' + T3, 'Temperature' + T4, 'Extra Temp Info' + T5, 'Humidity' + T6, 'Atmospheric Pressure' + T7, 'Wind' + T8, 'Cloud Percentage' + T9, 'Sunrise/Sunset'+ T10, Fore.LIGHTRED_EX + 'Back'])
        
        if setting == 'Coordinates' + T1:
            TCoord = not TCoord
        if setting == 'Weather' + T2:
            TWeather = not TWeather
        if setting == 'Country' + T3:
            TCountry = not TCountry
        if setting == 'Temperature' + T4:
            TTemp = not TTemp
        if setting == 'Extra Temp Info' + T5:
            TTempExtra = not TTempExtra
        if setting == 'Humidity' + T6:
            THumidity = not THumidity
        if setting == 'Atmospheric Pressure' + T7:
            TAtmosphericPressure = not TAtmosphericPressure
        if setting == 'Wind' + T8:
            TWind = not TWind
        if setting == 'Cloud Percentage' + T9:
            TCloudPercent = not TCloudPercent
        if setting == 'Sunrise/Sunset' + T10:
            TSunriseSunset = not TSunriseSunset
        if setting == Fore.LIGHTRED_EX + 'Back':
            loop = False
    
# Colours the Title cus its fun      
def menu_colour():
    global colour
    setting = menu('Colours', [Fore.LIGHTRED_EX + 'Red', Fore.BLUE + 'Blue', Fore.LIGHTCYAN_EX + 'Cyan', Fore.LIGHTMAGENTA_EX + 'Pink', Fore.LIGHTWHITE_EX + 'White'])
    if setting == Fore.LIGHTRED_EX + 'Red':
        colour = Fore.LIGHTRED_EX
    elif setting == Fore.BLUE + 'Blue':
        colour = Fore.BLUE
    elif setting == Fore.LIGHTCYAN_EX + 'Cyan':
        colour = Fore.LIGHTCYAN_EX
    elif setting == Fore.LIGHTMAGENTA_EX + 'Pink':
        colour = Fore.LIGHTMAGENTA_EX
    elif setting == Fore.LIGHTWHITE_EX + 'White':
        colour = Fore.LIGHTWHITE_EX

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

def PWeather(location):
    global debug, celcius, colour, TCoord, TWeather, TCountry, TTemp, TTempExtra, THumidity, TAtmosphericPressure, TWind, TCloudPercent, TSunriseSunset
    data = get_weather(location)
    if data['cod'] == 200:
        clear()
        if celcius == True:
            x = '°C'
        else:
            x = '°F'
        if TCountry == True:
            print(colour + Style.BRIGHT + f"Weather in {data['name']}, {data['sys']['country']}:\n" + Style.RESET_ALL)    
        else:
            print(colour + Style.BRIGHT + f"Weather in {data['name']}:\n" + Style.RESET_ALL)
        if TCoord == True:
            print(f"Coordinates: {data['coord']['lon']}, {data['coord']['lat']}")
        if TWeather == True:
            print(f"Weather: {data['weather'][0]['main']} ({data['weather'][0]['description']})".capitalize())
        if TTemp == True:
            print(f"Temperature: {data['main']['temp']} °F")    
        if TTempExtra == True:
            print(f"Feels like: {data['main']['feels_like']} " + x)
            print(f"Min Temp: {data['main']['temp_min']} " + x)
            print(f"Max Temp: {data['main']['temp_max']} " + x)
        if THumidity == True:
            print(f"Humidity: {data['main']['humidity']}%")
        if TAtmosphericPressure == True:
            print(f"Atmospheric Pressure: {data['main']['pressure']} hPa")
            print(f"Sea Level: {data['main']['sea_level']} hPa")
            print(f"Ground Level: {data['main']['grnd_level']} hPa")
        if TWind == True:
            print(f"Wind: {data['wind']['speed']} m/s")
        if TCloudPercent == True:
            print(f"Cloud Percentage: {data['clouds']['all']}%")
        if TSunriseSunset == True:
            print(f"Sunrise: {datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S')}")
            print(f"Sunset: {datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S')}")
        input('Press enter to continue\n')

# Menu to get weather
def menu_get_weather():
    global weatherLocations
    if weatherLocations == []:
        print (Fore.LIGHTRED_EX + 'No locations saved, please add a location' + Style.RESET_ALL)
        input('Press enter to continue\n')
        return
    else:
        selection = menu('Pick a saved location:', weatherLocations + [Fore.LIGHTRED_EX + 'Back'])
        PWeather(selection)

# Menu to pick a location
def menu_pick_location():
    global debug
    global weatherLocations
    loop = True
    while loop == True:
        if weatherLocations == []: # <--- Check if there are any locations saved, if not it goes straight to asking for a location
            x = inputLocation()
            if x == False:
                loop = False
                break
                    
        else:
            selection = menu('Saved Locations', ['Add a Location', 'Remove a Location', Fore.LIGHTRED_EX + 'Back'])
        
            if selection == Fore.LIGHTRED_EX + 'Back':
                loop = False
                break
            if selection == 'Add a Location':
                x = inputLocation()
                if x == False:
                    loop = False
                    break
            if selection == 'Remove a Location':
                removeLocation()
                       
# Settings menu            
def menu_settings():
    global debug
    global celcius
    setting = ''
    
    while setting != Fore.LIGHTRED_EX + 'Back':
        if debug == True:
            DOn = Fore.LIGHTGREEN_EX + ' ON'
        else:
            DOn = Fore.RED + ' OFF'
            
        if celcius == True:
            T = Fore.LIGHTGREEN_EX + '°C' + Fore.LIGHTWHITE_EX + ' < ' + Fore.LIGHTRED_EX + '°F'
        else:
            T = Fore.LIGHTRED_EX + '°C' + Fore.LIGHTWHITE_EX + ' > ' + Fore.LIGHTGREEN_EX + '°F'
            
        setting = menu('Settings', ['Temperature in ' + T, 'Debug Mode ' + DOn, 'Set Colour', 'Shown Information', Fore.LIGHTRED_EX + 'Back'])
        
        if setting == 'Debug Mode ' + DOn:
            if debug == True:
                debug = False
            else:
                debug = True
        
        if setting == 'Set Colour':
            menu_colour()
            
        if setting == 'Shown Information':
            menu_shown_information()
             
        if setting == 'Temperature in ' + T:
            if celcius == True:
                celcius = False
            else:
                celcius = True
                
    
    return

# Weather app using a menu
def menu_home():
    loop = True
    debug = False
    while loop == True:
        choice = menu('Weather App', ['Get Weather', 'Saved Locations', 'Settings', Fore.LIGHTRED_EX + 'Exit'])
        
        if choice == 'Get Weather':
            menu_get_weather()
            
        elif choice == 'Saved Locations':
            menu_pick_location()
            
        elif choice == 'Settings':
            menu_settings()
            
        elif choice == Fore.LIGHTRED_EX + 'Exit':
            print(Style.RESET_ALL + 'Goodbye!')
            exit()

# Run the weather app
try:
    menu_home()
except KeyboardInterrupt:
    print(Style.RESET_ALL + 'Goodbye!')
    exit()
except Exception as e:
    print(Style.RESET_ALL + 'An error occured:')
    print(Fore.LIGHTRED_EX + str(e) + Style.RESET_ALL)
    exit()
    
