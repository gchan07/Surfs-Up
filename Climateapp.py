import datetime as dt
import numpy as np
import pandas as pd
import json

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///./Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Create an app, being sure to pass __name__
app = Flask(__name__)

# Define what to do when a user hits `/api/v1.0/precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    year_ago = dt.date.today() - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date > year_ago).\
            order_by(Measurement.date).all()
    all_results = list(np.ravel(results))
    return jsonify(all_results)

# Define what to do when a user hits `/api/v1.0/stations route
@app.route("/api/v1.0/stations")
def stations():
    num_station = session.query(Station.station).count()
    return("There are " + str(num_station) + " stations") 

# Define what to do when a user hits `/api/v1.0/stations route
@app.route("/api/v1.0/tobs")
def tobs():
    results_tobs = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.date > year_ago).\
            order_by(Measurement.date).all()
    all_tobs = list(np.ravel(results_tobs))
    return jsonify(all_tobs) 

# Define what to do when a user hits `/api/v1.0/<start> route
@app.route("/api/v1.0/<start>")
def start():
    start_date = input("Start Date in %y-%m-%d")
    sel = [func.min(Measurement.tobs),
           func.max(Measurement.tobs),
           func.avg(Measurement.tobs)]    
    results = session.query(*sel).\
    filter(Measurement.date > start_date).\
    order_by(Measurement.date).all()
    print(results[0])
    return jsonify(results) 

if __name__ == "__main__":
    app.run(debug=True)
