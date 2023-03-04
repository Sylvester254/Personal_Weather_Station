from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from DataProcessor import app


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:toor@localhost/weatherData'  # database URI
db = SQLAlchemy(app)

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
