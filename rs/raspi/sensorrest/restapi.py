import flask_restplus
from werkzeug.exceptions import NotFound, BadRequest

from .sensorinfo import SensorApi


def init(api: flask_restplus.Api, sensors: SensorApi):
    ns = flask_restplus.namespace.Namespace(name="Sensors",
                                            path="/rest/sensors",
                                            description="Sensors REST API")

    sensorInfo = ns.model('SensorInfo', {
        'sensor_id': flask_restplus.fields.String,
        'name': flask_restplus.fields.String,
        'value': flask_restplus.fields.Float,
        'when': flask_restplus.fields.DateTime,
        'unit': flask_restplus.fields.String
    })

    @ns.route('/')
    class Sensors(flask_restplus.Resource):
        @ns.marshal_list_with(sensorInfo)
        def get(self):
            return list(sensors)

    @ns.route('/<string:sensor_id>')
    class Sensor(flask_restplus.Resource):
        @ns.marshal_with(sensorInfo)
        @ns.response(404, "If sensor id is not known")
        def get(self, sensor_id):
            try:
                return sensors[sensor_id]
            except (IndexError, KeyError):
                raise NotFound()
            
    @ns.route('/<string:sensor_id>/<int:value>')
    class SensorUpdate(flask_restplus.Resource):
        @ns.marshal_with(sensorInfo)
        @ns.response(404, "If sensor id is not known")
        def put(self, sensor_id, value):
            try:
                sensors[sensor_id] = value
                return sensors[sensor_id]
            except (IndexError, KeyError):
                raise NotFound()
            except TypeError:
                raise BadRequest()

    api.add_namespace(ns)
