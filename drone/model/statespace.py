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
        # self.speed = 0
        # self.course = 0
        self.vx = 0
        self.vy = 0
        self.vz = 0


    def serialize(self):
        return (""""lat": %s,"long": %s,"altitude": %s,
                    "roll": %s,"pitch":%s,"yaw": %s,
                    "vx":%s, "vy":%s, "vz":%s """
                % (self.lat, self.long, self.altitude,
                   self.roll, self.pitch, self.yaw,
                   self.vx,self.vy,self.vz))

    def log(self):
        sys.stderr.write(self.serialize())
        sys.stderr.flush()

    def __str__(self):
        return self.serialize()
