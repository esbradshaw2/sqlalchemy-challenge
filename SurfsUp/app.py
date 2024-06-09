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

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# reflect the tables


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

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
    # last 12 months precipitation data
    last_year_date = dt.date.today() - relativedelta(months=12)
    # Convert results to a dictionary
    # Assume data is stored in a variable named 'precipitation_data'
    precipitation_dict = {result.date: result.prcp for result in df_filtered}
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Assume station data is stored in a variable named 'station_data'
    stations_list = [station.station for station in station_data]
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query the dates and temperature observations of the most-active station for the previous year of data
    # Assume temperature data is stored in a variable named 'temperature_data'
    # Return a JSON list of temperature observations for the previous year
    return jsonify(temperature_data)

@app.route("/api/v1.0/<start>")
def temp_start(start):
    # Calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date
    # Assume temperature data is stored in a variable named 'temperature_data'
    return jsonify({"TMIN": min_temp, "TAVG": avg_temp, "TMAX": max_temp})

@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start, end):
    # Calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive
    # Assume temperature data is stored in a variable named 'temperature_data'
    return jsonify({"TMIN": min_temp, "TAVG": avg_temp, "TMAX": max_temp})

if __name__ == '__main__':
    app.run(debug=True)