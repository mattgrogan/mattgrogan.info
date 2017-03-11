+++
date = "2016-09-14"
title = "Python Geocoding Script"
draft = false
tags = ["Travel", "Python", "google-maps"]
+++

[Geocoder](https://github.com/mattgrogan/geocoder): A simple python script to access Google's Geocoding service.

The script has a simple purpose: retrieve the latitude and longitude coordinates for cities listed in a text file and save the coordinates to a json file.

The code uses the Geopy geocoding library at https://github.com/geopy/geopy

This json file is used for a Google Map embedded in a static web page.

## Usage
```
>python geocode.py -h
usage: geocode.py [-h] [-v] input_file output_file

A simple city geocoder

positional arguments:
  input_file     Input file (text)
  output_file    Output file (json)

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Verbose output
```

## Example

```
>python geocode.py example/cities.txt example/cities.json -v
Geocoding city New York, NY...
Finished geocoding New York, NY
Geocoding city London, England...
Finished geocoding London, England
Geocoding city Tokyo, Japan...
Finished geocoding Tokyo, Japan
Geocoding city Singapore...
Finished geocoding Singapore
Saving to example/cities.json
```
