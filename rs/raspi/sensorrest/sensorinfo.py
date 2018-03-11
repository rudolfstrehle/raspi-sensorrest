import typing
from datetime import datetime


class SensorInfo(object):
    def __init__(self, sensor_id: str, name: str, unit: str, value: float,
                 when: datetime=datetime.utcnow()):
        self.__name = name if name else sensor_id
        self.__id = sensor_id
        self.__unit = unit
        self.__value = value
        self.__when = when

    @property
    def name(self):
        return self.__name

    @property
    def sensor_id(self):
        return self.__id

    @property
    def unit(self):
        return self.__unit

    @property
    def value(self):
        return self.__value

    @property
    def when(self):
        return self.__when


SensorApi = typing.Collection[SensorInfo]
