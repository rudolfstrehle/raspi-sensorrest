from threading import Thread, Event
from .sensorinfo import SensorApi


class History:
    def __init__(self, sensors: SensorApi):
        self.__sensors = sensors
        self.__thread = Thread(target=self.__run, daemon=True)
        self.__stop = Event()
        self.__lock = Event()
        self.__thread.start()
        self.__frequency = 60

    def __run(self):
        while not self.__stop.wait(self.__frequency):
            self.__sensors = self.__poll_sensors()
