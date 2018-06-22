import requests
import json
from sys import argv
stops = []
vehicle = []

class Stop():
    def __init__(self, code, name, id):
        self.code = code
        self.name = name
        self.id = id

class Vehicle():
    def __init__(self, type, number):
        self.type = type
        self.number = number

def extractAllStops():
    rAllStop =requests.get('https://www.sofiatraffic.bg/interactivecard/stops/geo?bbox=25,51,27,53,EPSG:3857')
    allData = rAllStop.json()
    for stop in allData['features']:
        stops.append(Stop(stop['properties']['code'], stop['properties']['name'], stop['id']))

def schedule(code):
    for s in stops:
        if code == s.code:
            x = s.id

    step = {'stop_id' : x}
    rStop = requests.get('https://www.sofiatraffic.bg/interactivecard/virtual_panel?', params=step)
    dataForStop = rStop.json()

    for line in dataForStop['virtual_panel_data']['lines']:
        vehicle.append(Vehicle(line['transport'], line['name']))
        for z in line['cars']:
            departureTime = z['departure_time']
            vehicle[-1].time = departureTime

extractAllStops()
schedule('2731')


for v in vehicle:
    print(v.type, v.number, v.time)
