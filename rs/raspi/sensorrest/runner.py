from rs.raspi.sensorrest.restapi import init as rest
from flask.app import Flask
from flask_restplus.api import Api

try:
    from rs.raspi.sensorrest.w1sensors import W1Sensors
    sensors = W1Sensors()
except:  # @IgnorePep8
    from rs.raspi.sensorrest.dummysensors import DummySensors
    sensors = DummySensors()

if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app, title="Raspberri Pi Sensor REST API")
    rest(api, sensors)
    app.run(debug=True)
