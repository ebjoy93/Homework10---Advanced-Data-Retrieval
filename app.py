# import dependencies
import datetime as dt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model

Base = automap_base()

# reflect the tables

Base.prepare(engine, reflect=True)

# Save references to each table

Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Create app

app = Flask(__name__)

# route home and route options
@app.route("/Home")
def home():
    return (
               f"Available Routes: <br />"
               f"- Precipitation <br/>"
               f"/api/v1.0/precipitation <br />"
               f"- Stations <br/>"
               f"/api/v1.0/stations <br />"
               f"- Teampeature Observatinos (Tobs) <br/>"
               f"/api/v1.0/tobs <br />"
               f"- Start <br/>"
               f"/api/v1.0/<start> <br/>"
               f"- Temprature Information <br/>"
               f"/api/v1.0/<start>/<end> <br/>"
           )

@app.route("/api/v1.0/precipitation")
def prep():
    
    date_precip_scores = session.query(Measurement.date, Measurement.prcp)\
    filter(Measurement.date > '2016-08-23')\
    order_by(Measurement.date).all()

    df_date_precip_scores = pd.DataFrame(date_precip_scores)
    
    precip_dict = df_date_precip_scores.to_dict('records')

    precip_dict
    
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def station():
    
    stations = session.query(Station.station, Station.name).all()
    station_list = station_list = list(np.ravel(station))
    
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    dates_temp = session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23')\
    group_by(Measurement.station).all()
    
    return jsonify(dates_temp)

@app.route("/api/v1.0/<start>")
def calc_start(start):
        start_date = session.query(Station.id, Station.station, func.min(Measurement.tobs), func.max(Measurement.tobs),\
        func.avg(Measurement.tobs)).filter(Measurement.station == Station.station).filter(Measurement.date >= start).all()
       
        return jsonify(calc_start('2012-02-01'))
    
@app.route("/api/v1.0/<start>/<end>")
def calc_temps(start_date, end_date):
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
    filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    return jsonify(calc_temps('2012-02-01', '2012-02-10'))

if __name__ == "__main__":
    app.run(debug=True)