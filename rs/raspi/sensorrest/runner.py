from rs.raspi.sensorrest.restapi import init as rest
from flask.app import Flask
from flask_restplus.api import Api
from rs.raspi.sensorrest.dummysensors import DummySensors
from rs.raspi.sensorrest.w1sensors import W1Sensors

if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app, title="Raspberri Pi Sensor REST API")
#    sensors = DummySensors()
    sensors = W1Sensors()
    rest(api, sensors)
    app.run(debug=True)
