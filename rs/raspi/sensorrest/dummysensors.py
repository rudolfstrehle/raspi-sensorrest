from .sensorinfo import SensorInfo, SensorApi


class DummySensors(SensorApi):
    def __init__(self):
        self.__sensors = []
        self.__sensors.append(SensorInfo(
            name="Test 1", sensor_id="4711", value=24.1, unit="C"))
        self.__sensors.append(SensorInfo(
            name="Test 2", sensor_id="4712", value=23.5, unit="C"))

    def __len__(self):
        return self.__sensors.__len__()

    def __contains__(self, x):
        return self.__sensors.__contains__(x)

    def __iter__(self):
        return self.__sensors.__iter__()

    def items(self):
        return self.__sensors.items()

    def __getitem__(self, item):
        return [i for i in self if i.sensor_id == item][0]
