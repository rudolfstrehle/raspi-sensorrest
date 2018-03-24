from rs.raspi.sensorrest.restapi import init as rest
from flask.app import Flask
from flask_restplus.api import Api

try:
    from rs.raspi.sensorrest.w1sensors import W1Sensors
    w1sensors = W1Sensors()
except:  # @IgnorePep8
    from rs.raspi.sensorrest.dummysensors import DummySensors
    w1sensors = DummySensors()
    
from rs.raspi.sensorrest.gpio_sensors import GPIOSensors
from rs.raspi.sensorrest.aggregated_sensors import AggregatedSensors

gpiosensors = GPIOSensors({
    #0: 'i',
    #1: 'i',
    #2: 'i',
    #3: 'i',
    #4: 'i',
    #5: 'i',
    #6: 'i',
    #7: 'i',
    #8: 'i',
    #9: 'i',
    #10: 'i',
    #11: 'i',
    12: 'o0',
    #13: 'o0',
    #14: 'i',
    #15: 'i',
    #16: 'i',
    #17: 'i',
    #18: 'i',
    #19: 'i',
    20: 'o0',
    #21: 'o0',
    #22: 'i',
    #23: 'i',
    #24: 'i',
    #25: 'i',
    #26: 'i'
    })

def main():
    app = Flask(__name__)
    api = Api(app, title="Raspberri Pi Sensor REST API")
    rest(api, AggregatedSensors(w1sensors, gpiosensors))
    app.run(host='0.0.0.0')


if __name__ == '__main__':
    main()
