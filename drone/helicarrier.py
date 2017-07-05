import asyncio

import numpy

from .model.copterDynamics import rigid_transform_3D, getRollPitchYaw
from .model.thrustManager import ThrustManager
from .sensorconsole import SensorConsole
from .model.statespace import StateSpace


class HeliCarrier(object):
    def __init__(self):
        self.length = .25  # meters
        self.liftConstant = 1
        self.currentStateSpace = StateSpace()
        self.initialStateSpace = StateSpace()
        self.thrustManager = ThrustManager()
        self.state = 'stopped'
        self.log = False
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(SensorConsole().readSensorData(self))

    def start(self):
        self.thrustManager.startEngine()

    def stop(self):
        self.thrustManager.stopEngine()

    def getCurrentLocation(self):
        return self.currentStateSpace

    def moveTo(self, point):
        r, t = rigid_transform_3D(
            self.initialStateSpace.getVector(self.currentLocation),
            self.initialPlan.getVector(point)
        )
        roll, pitch, yaw = getRollPitchYaw(r)

    def getCorrectionVolt(self, roll, pitch, yaw):
        volt1, volt2, volt3, volt4 = 0
        # TODO
        return volt1, volt2, volt3, volt4

    def _manual(self, s1, s2, s3, s4):
        self.log = True
        print (self.currentStateSpace)
        print (s1, s2, s3, s4)
        self.thrustManager._manual(s1, s2, s3, s4)
        print (self.currentStateSpace)
