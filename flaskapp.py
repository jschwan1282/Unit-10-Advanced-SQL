import numpy as np
import datetime
import sqlalchemy
import json
from dateutil.relativedelta import relativedelta
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

#create the root
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start/<end>"

#create path for stations
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all results"""
    # Query all precipitation
    results = session.query(Measurement.date,Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list
    precip = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict[date] = prcp
        precip.append(precip_dict)
    return jsonify(precip)

#create path for stations
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all results"""
    # Query all stations
    results = session.query(Station.id,Station.name).all()

    session.close()

    # Create a dictionary from the row data and append to a list
    all_stations = []
    for id, names in results:
        station_dict = {}
        station_dict[id] = name
        all_stations.append(station_dict)
    return jsonify(all_stations)
    
#create path for stations
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all results"""
    # Query all stations
    results = session.query(Measurement.dates,Measurement.tobs).filter(Measurement.dates >= "2016-08-23", Measurement.dates <= "2017-08-23")

    session.close()

    # Create a dictionary from the row data and append to a list
    all_tobs = []
    for id, names in results:
        tobs_dict = {}
        tobs_dict [date] = name
        all_tobs .append(tobs_dict )
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def daterangestart(start=None):
    # check that date is properly formatted
    try:
        start = datetime.datetime.strptime(start, '%Y-%m-%d')
    except:
        return("Incorrect start date, format should be YYYY-MM-DD")

    # open session get results from start to last date (last_day)
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs),func.round(func.avg(Measurement.tobs),1),func.max(Measurement.tobs)).filter(Measurement.date.between(start - relativedelta(days=1), last_day + relativedelta(days=1)))
    session.close()

    all_tobs = []
    for mint, avgt, maxt in results:
        tobs_dict = {}
        tobs_dict["Min Temp"] = mint
        tobs_dict["Avg Temp"] = avgt
        tob_dict["Max Temp"] = maxt
        all_tobs.append(tobs_dict)
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>/<end>")
def daterangestartend(start=None, end=None):
    # check that date is properly formatted
    try:
        start = datetime.datetime.strptime(start, '%Y-%m-%d')
    except:
        return("Incorrect start date, format should be YYYY-MM-DD")

    try:
        end = datetime.datetime.strptime(end, '%Y-%m-%d')
    except:
        return("Incorrect start date, format should be YYYY-MM-DD")
    
    # open session get results from start to last date (last_day)
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs),func.round(func.avg(Measurement.tobs),1),func.max(Measurement.tobs)).filter(Measurement.date.between(start - relativedelta(days=1), end + relativedelta(days=1)))
    session.close()

    all_tobs = []
    for mint, avgt, maxt in results:
        tobs_dict = {}
        tobs_dict["Max Temp"] = maxt
        tobs_dict["Avg Temp"] = avgt
        tobs_dict["Min Temp"] = mint
        filtered_tob.append(tob_dict)
    return jsonify(all_tobs)

if __name__ == "__main__":
    app.run(debug=True)