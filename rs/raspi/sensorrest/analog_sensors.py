from .sensorinfo import SensorInfo, SensorApi
from threading import Thread, Event, Lock

try:
    from spidev import SpiDev
except:
    class SpiDev:
        def open(self, *args):
            pass
        
        def xfer2(self, *args):  # @UnusedVariable
            return [0, 0, -1]


class AnalogSensors(SensorApi):
    def __init__(self):
        self.__spi = SpiDev()
        self.__spi.open(0,0)
        self.__sensors = []
        self.__thread = Thread(target=self.__run, daemon=True)
        self.__stop = Event()
        self.__lock = Lock()
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
            self.__update_sensors()
            
    def __update_sensors(self):
        sensors = self.__poll_sensors()
        with self.__lock:
            self.__sensors = sensors
            
    def __readadc(self, adcnum):
        r = self.__spi.xfer2([1,8+adcnum <<4,0])
        adcout = ((r[1] &3) <<8)+r[2]
        return adcout

    def __get_values(self):
        values = {}
        for i in range(8):
            name = 'analog-{}'.format(i)
            values[name] = self.__readadc(i)
        return values

    def __poll_sensors(self):
        sensors = [SensorInfo(sensor_id=k, value=v, unit="C")
                   for k, v in self.__get_values().items()]
        return sensors
