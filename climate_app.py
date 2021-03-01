import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station=Base.classes.station
app = Flask(__name__)
@app.route("/")
def Home():
    return (
        f"Welcome to the Hawaii Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation <br>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start_end")

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query most recent 12 months precipitation data
    prcp_data=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>='2016-08-23').all()

    session.close()
    
    prcp_json = []
    for date, prcp in prcp_data:
       prcp_dict = {}
       prcp_dict["date"] = date
       prcp_dict["prcp"] = prcp
       prcp_json.append(prcp_dict)

    # Convert list of tuples into normal list

    return jsonify(prcp_json)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query most recent 12 months precipitation data
    station_data=session.query(Station.station, Station.name).all()

    session.close()
    
    station_json = []
    for station, name in station_data:
       station_dict = {}
       station_dict["station"] = station
       station_dict["name"] = name
       station_json.append(station_dict)

    # Convert list of tuples into normal list

    return jsonify(station_json)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query most recent 12 months precipitation data
    temp_data_active=session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>='2016-08-18').filter(Measurement.station=='USC00519281').all()
    session.close()
    
    temp_json = []
    for date, tobs in temp_data_active:
       temp_dict = {}
       temp_dict["date"] = date
       temp_dict["tobs"] = tobs
       temp_json.append(temp_dict)

    # Convert list of tuples into normal list

    return jsonify(temp_json)


@app.route("/api/v1.0/<start_date>")
def Start_date(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of min, avg and max tobs for a start date"""
    # Query all tobs

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of start_date_tobs
    start_date_tobs = []
    for min, avg, max in results:
        start_date_tobs_dict = {}
        start_date_tobs_dict["min_temp"] = min
        start_date_tobs_dict["avg_temp"] = avg
        start_date_tobs_dict["max_temp"] = max
        start_date_tobs.append(start_date_tobs_dict) 

    return jsonify(start_date_tobs)


@app.route("/api/v1.0/<start_date>/<end_date>")
def Start_end_date(start_date, end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of min, avg and max tobs for start and end dates"""
    # Query all tobs

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()
  
    # Create a dictionary from the row data and append to a list of start_end_date_tobs
    start_end_tobs = []
    for min, avg, max in results:
        start_end_tobs_dict = {}
        start_end_tobs_dict["min_temp"] = min
        start_end_tobs_dict["avg_temp"] = avg
        start_end_tobs_dict["max_temp"] = max
        start_end_tobs.append(start_end_tobs_dict) 
    

    return jsonify(start_end_tobs)


if __name__ == "__main__":
    app.run(debug=True)


