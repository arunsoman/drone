import asyncio

import model.statespace
import numpy

import pinointerface as ch
import sensor
from model.copterDynamics import rigid_transform_3D, getRollPitchYaw
from model.motor import Motor
from model.thrustManager import ThrustManager


class HeliCarrier(object):
    def __init__(self):
        self.length = .25 #meters
        self.liftConstant = 1
        self.currentStateSpace = model.statespace()
        self.initialStateSpace = model.StateSpace()
        self.roll = 0
        self.pitch = 0
        self.yaw = 0
        self.thrustManager = ThrustManager()
        self.gps = sensor.GPS()
        self.bmp = sensor.BMP180()
        self.gyro = sensor.GY521()
        self.compass = sensor.HMC5883L()
        self.state = 'stopped'
        self.loop = asyncio.get_event_loop()
        self.loop.call_soon(self.__readSensorData(), self.loop)
        self.loop.run_forever()
        self.log = False

    asyncio.coroutine
    def __readSensorData(self):
        lat, long = self.gps.getLatLong()
        self.initialStateSpace.lat = lat
        self.initialStateSpace.long = long
        self.initialStateSpace.altitude = self.bmp.getAltitude()
        roll, pitch = self.gyro.getRollPitch()
        self.initialStateSpace.roll = roll
        self.initialStateSpace.pitch = pitch
        self.initialStateSpace.yaw = self.compass.getYaw()

        while self.state is not 'stopped':
            lat, long = self.gps.getLatLong()
            self.currentStateSpace.lat = lat
            self.currentStateSpace.long = long
            self.currentStateSpace.altitude = self.bmp.getAltitude()
            roll, pitch = self.gyro.getRollPitch()
            self.currentStateSpace.roll = roll
            self.currentStateSpace.pitch = pitch
            self.currentStateSpace.yaw = self.compass.getYaw()
            if self.log:
                self.currentStateSpace.log()




    def start(self):
        self.thrustManager.startEngine()

    def stop(self):
        self.thrustManager.stopEngine()

    def getCurrentLocation(self):
        return self.currentStateSpace


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

    def __manual(self, s1, s2, s3, s4):
        self.log = True
        print (self.currentStateSpace)
        print (s1,s2,s3,s4)
        self.thrustManager.__manual(s1, s2, s3, s4)
        print (self.currentStateSpace)
