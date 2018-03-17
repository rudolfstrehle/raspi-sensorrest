import typing
from datetime import datetime


class SensorInfo(object):
    def __init__(self, sensor_id: str, name: str = None, unit: str = None,
                 value: float = None,
                 when: datetime=None):
        self.__name = name if name else sensor_id
        self.__id = sensor_id
        self.__unit = unit
        self.__value = value
        self.__when = when if when else datetime.utcnow()

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


SensorApi = typing.Iterable[SensorInfo]
