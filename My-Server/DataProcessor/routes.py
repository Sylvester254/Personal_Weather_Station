from DataProcessor.models import SensorData
from DataProcessor.models import db
from flask import render_template, request
from DataProcessor import app
from DataProcessor.routes import *


@app.route("/index")
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/dht22', methods=['POST'])
def dht22():
    data = request.json # get data from the raspberry
    temperature = data['temperature']
    humidity = data['humidity']
    
    # create a new instance of SensorData with the received data
    new_data = SensorData(temperature=temperature, humidity=humidity)
    print(new_data)
    
    # add the new instance to the database
    db.session.add(new_data)
    db.session.commit()
    print('Data stored successfully!')
    
    return 'Data received and stored successfully!'