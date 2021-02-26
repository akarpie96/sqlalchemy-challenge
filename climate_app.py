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

app = Flask(__name__)
@app.route("/")
def Home():
    return (
        f"Welcome to the Hawaii Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation <br>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>")


if __name__ == "__main__":
    app.run(debug=True)


    Base.classes.keys()
