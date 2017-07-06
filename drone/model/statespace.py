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

    def getVector(self, sp):
        return numpy.array([self.lat - sp.lat,
                            self.long - sp.long,
                            self.altitude - sp.altitude])

    def get_state_dict(self):
        return {'lat': self.lat,
                'long': self.long,
                'altitude': self.altitude,
                'roll': self.roll,
                'pitch': self.pitch,
                'yaw': self.yaw
                }

    def log(self):
        # for testing
        sys.stderr.write(
            "pitch: %s\troll: %s\tyaw: %s\tlat: %s\tlong: %s\talti: %s          \r"
            % (self.pitch, self.roll, self.yaw, self.lat, self.long, self.altitude))
        sys.stderr.flush()
