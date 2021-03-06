# Dependencies
import datetime as dt 
import numpy as np 
import pandas as pd 

# Dependencies from sqlalchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Dependencies from flask
from flask import Flask, jsonify

# Access the sqlite database
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect database into classes
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement 
Station = Base.classes.station 

# Create our session (link) from Python to the DB
session = Session(engine)

# Define the flask app
app = Flask(__name__)

# Define the welcome root
@app.route('/')

# Build the welcome root
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API! <Br>
    Available Routes: <Br>
    /api/v1.0/precipitation <Br>
    /api/v1.0/stations <Br>
    /api/v1.0/tobs <Br>
    /api/v1.0/temp/start/end <Br>
    ''')

# Percipitation analysis route
@app.route("/api/v1.0/precipitation")

# Define the precipitation function
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# Stations route
@app.route("/api/v1.0/stations")

# Define the stations function
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations)

# Temperature Observations route
@app.route("/api/v1.0/tobs")

# Define the temp obs function
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

# Temp statistics route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# Define the stats function
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        results = session.query(*sel).filter(Measurement.date <= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

if __name__ == '__main__':
    app.run(debug=True)