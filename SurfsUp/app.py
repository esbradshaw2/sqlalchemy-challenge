# Import the dependencies.
from flask import Flask, jsonify
import datetime as dt
from dateutil.relativedelta import relativedelta
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from dateutil.relativedelta import relativedelta

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect existing database into new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session from Python to database
session = Session(engine)

# Query databases
precipitation_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23').\
    filter(Measurement.date <= '2017-08-23').all()

stations_data = session.query(Station.station, Station.name).all()

most_active_station = session.query(Measurement.station).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).first()[0]

tobs_data = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == most_active_station).\
    filter(Measurement.date >= '2016-08-23').\
    filter(Measurement.date <= '2017-08-23').all()

# Create dictionaries/lists from query results
precipitation_dict = {}
for date, prcp in precipitation_data:
    precipitation_dict[date] = prcp

stations_list = []
for station, name in stations_data:
    stations_list.append({
        "station": station,
        "name": name
    })

tobs_list = []
for date, tobs in tobs_data:
    tobs_list.append({
        "date": date,
        "tobs": tobs
    })

# Calculate temps
def calculate_temps(start_date, end_date=None):
    if end_date:
        temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    else:
        temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).all()

    return temps

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    return (
        f"Welcome to the Climate App API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start_date_temps(start):
    temps = calculate_temps(start)
    return jsonify({"min_temp": temps[0][0], "avg_temp": temps[0][1], "max_temp": temps[0][2]})


@app.route("/api/v1.0/<start>/<end>")
def start_end_dates_temps(start, end):
    temps = calculate_temps(start, end)
    return jsonify({"min_temp": temps[0][0], "avg_temp": temps[0][1], "max_temp": temps[0][2]})


if __name__ == '__main__':
    app.run(debug=True)