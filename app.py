#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
import requests
# create app
app = Flask(__name__)

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


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'GET':
        # show html form
        return '''
            <form method="post">
                <input type="text" name="expression" />
                <input type="submit" value="Calculate" />
            </form>
        '''
    elif request.method == 'POST':
        expression = request.form.get('expression')
        result = eval(expression)
        result = square(result)
        extractAllStops()
        schedule(2132)
        return 'result: %s' % result

@app.route('/result')
def result():
    time = vehicle[-1].time
    type = vehicle[-1].type
    number = vehicle[-1].number
    return render_template('index.html', time = time, type = type, number = number)

def square(a):
    a = a*a
    return a

# run app
if __name__ == '__main__':
    app.run()