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

engine = create_engine("sqlite:///Resources/hawaii.sqlite?check_same_thread=False")

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
@app.route("/")
def home():
    return (
               f"Available Routes: <br />"
               f"- Precipitation<br/>"
               f"/api/v1.0/precipitation<br />"
               f"- Stations<br/>"
               f"/api/v1.0/stations<br />"
               f"- Teampeature Observatinos (Tobs)<br/>"
               f"/api/v1.0/tobs<br />"
               f"- Start<br/>"
               f"/api/v1.0/<start><br/>"
               f"- Temprature Information<br/>"
               f"/api/v1.0/<start>/<end> <br/>"
           )

@app.route("/api/v1.0/precipitation")
def prep():
    
    date_precip_scores = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-23').order_by(Measurement.date).all()

    df_date_precip_scores = pd.DataFrame(date_precip_scores)
    
    precip_dict = df_date_precip_scores.to_dict('records')

    precip_dict
    
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def station():
    
    station_list = session.query(Station.station, Station.name).group_by(Station.station).all()
    #station_list = list(np.ravel(station))
    
    print(station_list)
    
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    dates_temp = session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23').group_by(Measurement.station).all()
    
    print(dates_temp)
    
    return jsonify(dates_temp)

@app.route("/api/v1.0/<start>")
def calc_start(start):
        start_date = session.query(Station.id, Station.station, func.min(Measurement.tobs), func.max(Measurement.tobs),\
        func.avg(Measurement.tobs)).filter(Measurement.station == Station.station).filter(Measurement.date >= start).all()
        
        df_start_date = pd.DataFrame(start_date).transpose()
        #start_date_dict = df_start_Date.to_dict('list')
        
        print(df_start_date)
       
        return jsonify(df_start_date)
    
@app.route("/api/v1.0/<start>/<end>")
def calc_temps(start_date, end_date):
    calc_temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    print(calc_temps)

    return jsonify(calc_temps)

if __name__ == "__main__":
    app.run(debug=True)