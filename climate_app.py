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
        f"/api/v1.0/tobs<br/>")

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
if __name__ == "__main__":
    app.run(debug=True)


    # Base.classes.keys()