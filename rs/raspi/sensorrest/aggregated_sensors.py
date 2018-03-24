from .sensorinfo import SensorApi


class AggregatedSensors(SensorApi):
    def __init__(self, *args):
        self.__backends = args

    def __len__(self):
        l = 0
        for b in self.__backends:
            l = l + len(b)
        return l

    def __contains__(self, x):
        for b in self.__backends:
            if x in b:
                return True
        return False

    def __getitem__(self, item):
        for b in self.__backends:
            if item in b:
                return b[item]
        raise KeyError
    
    def __setitem__(self, key, value):
        for b in self.__backends:
            if key in b:
                b[key] = value
                return
        raise KeyError

    def __iter__(self):
        values = []
        for b in self.__backends:
            for i in b:
                values.append(i)
        return list(values).__iter__()
