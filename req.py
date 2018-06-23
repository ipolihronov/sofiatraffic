# -*- coding: utf-8 -*-
import requests
import json
import urllib.request
stops = []
vehicle = []

class Stop():
    def __init__(self, code, name, id):
        self.code = code
        self.name = name
        self.id = id

class Vechile():
    def __init__(self, type, number):
        self.type = type
        self.number = number
    time = []

def extractAllStops():
    # rAllStop = requests.get('https://www.sofiatraffic.bg/interactivecard/stops/geo?bbox=25,51,27,53,EPSG:3857,EPSG:3857')
    # allData = rAllStop.json()
    # with open('stopsCache.json', 'w') as outfile:
    #     json.dump(allData, outfile)

    with open('stopsCache.json') as f:
        data = json.load(f)
    for stop in data['features']:
        stops.append(Stop(stop['properties']['code'], stop['properties']['name'], stop['id']))

def schedule(code):
    for s in stops:
        if code == s.code:
            x = s.id

    step = {'stop_id' : x}
    rStop = requests.get('https://www.sofiatraffic.bg/interactivecard/virtual_panel?', params=step)
    dataForStop = rStop.json()

    lineIndex = 0
    for line in dataForStop['virtual_panel_data']['lines']:
        vehicle.append(Vechile(line['transport'], line['name']))
        print(vehicle[lineIndex].type, vehicle[lineIndex].number)
        lineIndex += 1
        for z in line['cars']:
            departureTime = z['departure_time']
            print(departureTime)

extractAllStops()
schedule(879)

# for v in vehicle:
#     print(v.type, v.number, v.time)
