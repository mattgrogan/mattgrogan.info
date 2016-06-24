# Python script to geocode city names
# Usage: python geocode.py input.txt output.txt 
from geopy.geocoders import GoogleV3
from json import dump, load
from time import sleep
from sys import argv
import os

class City_Cache(object):
    """ Holds cache of various city and lat/long """
    
    def __init__(self):
        """ Initialize the cache """
        
        self._data = {}
        
    def load(self, filename):
        """ Load values from filename """
        print "Loading from %s" % filename
        
        with open(filename, 'r') as input_file:
            self._data = load(input_file)
    
    def save(self, filename):
        """ Save values to filename (overwrite) """
        print "Saving to %s" % filename
        
        with open(filename, 'w') as output_file:
            dump(self._data, output_file, sort_keys=True, indent=4, 
                 separators=(',', ': '))
    
    def add_city(self, city, timeout = 1):
        """ Add city if it does not exist in the cache """
        
        city = city.strip()
        
        if city in self._data.keys():
            print "City %s is cached" % city
        else:
            print "Geocoding city %s..." % city
            
            geolocator = GoogleV3()
            location = geolocator.geocode(city)
            
            city_data = {
                'city': city,
                'formatted_address': location.raw['formatted_address'],
                'latitude': location.latitude,
                'longitude': location.longitude
            }
            
            self._data[city] = city_data
            
            print "Finished geocoding %s" % city
            
            sleep(timeout)
 
if __name__ == "__main__":
    
    input_file_name = argv[1]
    output_file_name = argv[2]
    
    cache = City_Cache()
    
    if os.path.isfile(output_file_name):
        cache.load(output_file_name)
    
    with open(input_file_name, 'r') as input_file:
        cities = input_file.readlines()
        
    for city in cities:
        cache.add_city(city)
        
    cache.save(output_file_name)
