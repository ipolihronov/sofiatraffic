#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import request
from req import schedule, extractAllStops
from req import vehicle, stopName

# create app
app = Flask(__name__)

import requests

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'GET':
        # show html form
        return '''
            <form method="post">
                <p> Въведи номер на спирката </p>
                <input type="text" name="expression" />
                <input type="submit" value="Готово" />
            </form>
        '''
    elif request.method == 'POST':
        expression = request.form.get('expression')
        try:
            result = eval(expression)
        except:
            return render_template('problem.html')
        extractAllStops()
        try:
            schedule(result)
        except:
            return render_template('problem.html')
        print(stopName)
        return render_template('index.html', vehicle = vehicle, stopName = stopName)


# run app
if __name__ == '__main__':
    app.run()