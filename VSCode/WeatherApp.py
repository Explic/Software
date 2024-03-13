import pick
from pick import pick 
from colorama import Fore, Back, Style
import requests


def setcolor(text, color):
    return color + text

def rcolor():
    return print(Style.RESET_ALL + '')



def menu(title, options):
    
    pick(options, title)
    
print(setcolor('hi', Fore.BLUE))
menu('Weather App', [tcolor('Get Weather', Fore.RED), 'Exit'])

rcolor()


