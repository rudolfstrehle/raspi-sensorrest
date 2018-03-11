from flask_restplus import Resource, Api, fields
from flask_restplus.namespace import Namespace
from werkzeug.exceptions import NotFound

from .sensorinfo import SensorApi


def init(api: Api, sensors: SensorApi):
    ns = Namespace(name="Sensors", path="/rest/sensors",
                   description="Sensors REST API")

    sensorInfo = ns.model('SensorInfo', {
        'sensor_id': fields.String,
        'name': fields.String,
        'value': fields.Float,
        'when': fields.DateTime,
        'unit': fields.String
    })

    @ns.route('/')
    class Sensors(Resource):
        @ns.marshal_list_with(sensorInfo)
        def get(self):
            return list(sensors)

    @ns.route('/<string:sensor_id>')
    class Sensor(Resource):
        @ns.marshal_with(sensorInfo)
        @ns.response(404, "If sensor id is not known")
        def get(self, sensor_id):
            try:
                return sensors[sensor_id]
            except IndexError:
                raise NotFound()

    api.add_namespace(ns)
