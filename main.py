from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# configure sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databasestorage.sql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# defining data model
class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    light = db.Column(db.Float)
    no = db.Column(db.Float)
    no2 = db.Column(db.Float)
    o3 = db.Column(db.Float)
    pm1 = db.Column(db.Float)
    pm10 = db.Column(db.Float)
    pm2p5 = db.Column(db.Float)
    pressure = db.Column(db.Float)
    rain = db.Column(db.Float)
    rain_d = db.Column(db.Float)
    rain_total = db.Column(db.Float)
    rh = db.Column(db.Float)
    so2 = db.Column(db.Float)
    sound = db.Column(db.Float)
    temperature = db.Column(db.Float)
    timestamp = db.Column(db.BigInteger)
    ts = db.Column(db.BigInteger)
    uva = db.Column(db.Float)
    uvb = db.Column(db.Float)
    voc = db.Column(db.Float)
    aqi = db.Column(db.Float)
    co2 = db.Column(db.Float)
    devID = db.Column(db.String)

def seed_database():
    sample_data = SensorData(
        light=166.3138,
        no=52.5271,
        no2=10,
        o3=0.02,
        pm1=8,
        pm10=12,
        pm2p5=11,
        pressure=980.096,
        rain=0,
        rain_d=None,
        rain_total=1860.8,
        rh=79,
        so2=0.001,
        sound=26.5491,
        temperature=31.5,
        timestamp=1713157818394,
        ts=1710682333367,
        uva=0.0182,
        uvb=0.1092,
        voc=0,
        aqi=84.0,
        co2=460.0,
        devID="EMS0017"
    )
    
    db.session.add(sample_data)
    db.session.commit()

@app.route('/api/sensordata', methods=['GET'])
def get_sensor_data():
    # fetch data from database
    data = SensorData.query.filter_by(devID="EMS0017").first()
    
    if not data:
        return jsonify({"error": "No data found"}), 404

    # convert database data to the desired format
    output = [
        {"name": "time", "value": data.timestamp},
        {"name": "Light", "unit": "lux", "value": data.light},
        {"name": "CH₂O", "unit": "mg/m³", "value": data.voc},
        {"name": "CO", "unit": "ppm", "value": data.no},
        {"name": "CO₂", "unit": "ppm", "value": data.co2},
        {"name": "Humidity", "unit": "%", "value": data.rh},
        {"name": "NO₂", "unit": "ppm", "value": data.no2},
        {"name": "O₃", "unit": "ppm", "value": data.o3},
        {"name": "PM1.0", "unit": "μg/m³", "value": data.pm1},
        {"name": "PM10", "unit": "μg/m³", "value": data.pm10},
        {"name": "PM2.5", "unit": "μg/m³", "value": data.pm2p5},
        {"name": "Pressure", "unit": "hPa/mb", "value": data.pressure},
        {"name": "SO₂", "unit": "ppm", "value": data.so2},
        {"name": "Sound", "unit": "db", "value": data.sound},
        {"name": "TVOC", "unit": "grade", "value": data.voc},
        {"name": "Temperature", "unit": "°C", "value": data.temperature},
        {"name": "UVI", "unit": "mW/cm²", "value": data.uva + data.uvb},
        {"interpretation": "Satisfactory - Minor breathing discomfort to sensitive people", "name": "AQI", "value": data.aqi}
    ]
    
    return jsonify(output)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not SensorData.query.first():
            seed_database()
    app.run(debug=True)