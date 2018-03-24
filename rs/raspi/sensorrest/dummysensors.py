from random import random
from threading import Thread, Event

from .sensorinfo import SensorInfo, SensorApi


class DummySensors(SensorApi):
    def __init__(self):
        self.__sensors = []
        self.__thread = Thread(target=self.__run, daemon=True)
        self.__stop = Event()
        self.__thread.start()

    def __del__(self):
        self.__stop.set()
        self.__thread.join(10)

    def __len__(self):
        return self.__sensors.__len__()

    def __contains__(self, item):
        return len([i for i in self if i.sensor_id == item]) > 0

    def __iter__(self):
        return self.__sensors.__iter__()

    def __getitem__(self, item):
        return [i for i in self if i.sensor_id == item][0]

    def __run(self):
        while not self.__stop.wait(1):
            self.__sensors = self.__poll_sensors()

    def __get_values(self):
        values = {}
        for i in range(int(10 * random())):
            values["random-" + str(i)] = 20 + random() * 10
        return values

    def __poll_sensors(self):
        sensors = [SensorInfo(sensor_id=k, value=v, unit="C")
                   for k, v in self.__get_values().items()]
        return sensors
