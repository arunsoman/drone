import asyncio
import numpy

import pinointerface as ch
from model.copterDynamics import rigid_transform_3D, getRollPitchYaw
from model.motor import Motor


class HeliCarrier(object):
    def __init__(self):
        self.length = .25 #meters
        self.liftConstant = 1
        self.currentLocation = self.getCurrentLocation()
        self.initialFramme = self.currentLocation
        self.initialPlan = []
    def getCurrentLocation(self):
        return [
            self.gps.x,
            self.gps.y,
            self.altimeter.altitude]

    def totalTorque(self):
        torque = 0
        for motor in self.motors:
            torque+= motor.torque()
        return torque

    def torqueComponents(self):
        lk = self.length*self.liftConstant
        return [
            lk*(-self.m2.torqueSq()+self.m4.torqueSq()),
            lk*(-self.m1.torqueSq()+self.m3.torqueSq()),
            self.totalTorque()
                ]

    def moveTo(self, point):
        r,t = rigid_transform_3D(
            numpy.array(self.initialPlan - self.currentLocation),
            numpy.array(self.initialPlan - point)
        )
        roll, pitch, yaw = getRollPitchYaw(r)

    def getCorrectionVolt(self, roll, pitch, yaw):
        volt1, volt2, volt3, volt4 = 0
        #TODO
        return volt1, volt2, volt3, volt4