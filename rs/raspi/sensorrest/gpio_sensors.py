from .sensorinfo import SensorInfo, SensorApi
from threading import Thread, Event, Lock
from random import random

try:
    import RPi.GPIO as GPIO  # @UnresolvedImport
except:
    class GPIO:
        BCM = 0
        IN = 0
        OUT = 0
        PUD_UP = 0
        
        @classmethod
        def input(cls, pin):  # @UnusedVariable
            return int(random() * 2)
        
        @staticmethod
        def setmode(*args):
            pass
        
        @staticmethod
        def setup(*args, **kvargs):
            pass
        
        @staticmethod
        def output(*args):
            pass


class GPIOSensors(SensorApi):
    def __init__(self, io):
        self.__sensors = []
        self.__thread = Thread(target=self.__run, daemon=True)
        self.__stop = Event()
        self.__io = io
        self.__output = {}
        self.__lock = Lock()

        GPIO.setmode(GPIO.BCM)
        
        for k, v in io.items():  # @UnusedVariable
            l = v.lower()
            if l.startswith('i'):
                GPIO.setup(int(k), GPIO.IN)
            else:
                GPIO.setup(int(k), GPIO.OUT, initial=int(l[1]))
                self.__output[int(k)] = int(l[1])
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

    def __setitem__(self, key, value):
        i = int(key[5:])
        with self.__lock:
            GPIO.output(i, value)
            self.__output[i] = value
        self.__update_sensors()

    def __run(self):
        while not self.__stop.wait(1):
            self.__update_sensors()
            
    def __update_sensors(self):
        sensors = self.__poll_sensors()
        with self.__lock:
            self.__sensors = sensors

    def __get_values(self):
        values = {}
        with self.__lock:
            for k, v in self.__output.items():
                name = 'gpio-{}'.format(k)
                values[name] = v
        for k, v in self.__io.items():
            if v.lower().startswith("i"):
                name = 'gpio-{}'.format(k)
                values[name] = GPIO.input(k)
        return values

    def __poll_sensors(self):
        sensors = [SensorInfo(sensor_id=k, value=v, unit="")
                   for k, v in self.__get_values().items()]
        return sensors
