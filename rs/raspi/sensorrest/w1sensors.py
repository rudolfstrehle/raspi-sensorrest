from .sensorinfo import SensorInfo, SensorApi
from threading import Thread, Event
import RPi.GPIO as GPIO  # @UnresolvedImport
import glob
import time


class W1Sensors(SensorApi):
    def __init__(self):
        self.__sensors = []
        self.__thread = Thread(target=self.__run, daemon=True)
        self.__stop = Event()

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.__thread.start()

    def __del__(self):
        self.__stop.set()
        self.__thread.join(10)

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

    def __run(self):
        while not self.__stop.wait(1):
            self.__sensors = self.__poll_sensors()

    def __get_device_folders(self, base_dir):
        while True:
            try:
                device_folder = glob.glob(base_dir + '28*/w1_slave')
                return device_folder
            except IndexError:
                time.sleep(0.5)

    def __read_lines(self, path):
        with open(path, 'r') as f:
            lines = f.readlines()
            f.close()
            return lines

    def __get_values(self, files):
        values = {}
        for f in files:
            name = f.split("/")[-2]
            lines = self.__read_lines(f)
            if lines is not None and len(lines) == 2 and "YES" in lines[0]:
                values[name] = float(lines[1].split("=")[1]) / 1000.0
        return values

    def __poll_sensors(self):
        base_dir = '/sys/bus/w1/devices/'

        sensors = [SensorInfo(sensor_id=k, value=v, unit="C")
                   for k, v in self.__get_values(
                       self.__get_device_folders(base_dir)).items()]
        return sensors
