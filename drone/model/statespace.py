import numpy
import sys


class StateSpace(object):
    def __init__(self):
        self.lat = 0
        self.long = 0
        self.altitude = 0
        self.roll = 0
        self.pitch = 0
        self.yaw = 0
        self.speed = 0
        self.heading = {}

    def serialize(self):
        return (""""lat": %s,"long": %s,"altitude": %s,
                    "roll": %s,"pitch":%s,"yaw": %s,
                    "speed":%s, "heading":%s """
                % (self.lat, self.long, self.altitude,
                   self.roll, self.pitch, self.yaw,
                   self.speed, self.heading))

    def log(self):
        sys.stderr.write(self.serialize())
        sys.stderr.flush()
