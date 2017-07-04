import numpy


class StateSpace(object):
    def __init__(self):
        self.lat = 0
        self.long = 0
        self.altitude = 0
        self.roll  = 0
        self.pitch = 0
        self.yaw   = 0

    def getVector(self, sp):
        return numpy.array([self.lat-sp.lat,
                            self.long - sp.long,
                            self.altitude - sp.altitude])

    def log(self):
        pass



