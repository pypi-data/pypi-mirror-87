import json
import requests
import pandas as pd
import os

# Usage example of a geolocalizer
# localizer = GPS()
# lat, long = localizer.get_coordinates()
# print(lat, lng)
class GPS():
    def __init__(self, coordinates_source='https://api.3geonames.org/.json?randomland=yes'): 
        res = requests.get(coordinates_source).json()
        self.coordinates = { "lat": res['nearest']['latt'], "lng": res['nearest']['longt'] }

    def get_coordinates(self):
        return self.coordinates


class LCD1602:
    def __init__(self):
        print(" [.] Created LCD1602")

    def write_line(self, line, data, align='LEFT'):
        print(" [.] Write line", line, data, align)


class RGB():
    def __init__(self):
        print(" [+] Created a virtual RGB led")

    def write(self, color):
        print(" [.] Update RGB led state to", color)


'''# Usage example
import time
wheels = Wheels()

wheels.forward()

time.sleep(5)
wheels.stop()

wheels.right()
time.sleep(2)

wheels.left()
time.sleep(2)

wheels.backward()

time.sleep(2)
wheels.stop()
'''
class Wheels():

    def __init__(self):
        print(" [.] Created left and right wheel in stop position")


    def stop(self):
        print(" [.] Stop wheels")


    def forward(self):
        print(" [.] Forward wheels")


    def right(self):
        print(" [.] Move right")
        

    def left(self):
        print(" [.] Move left")

    
    def backward(self):
        print(" [.] Move backward")

