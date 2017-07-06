import asyncio

from .sensor import (GPS, BMP180, GY521, HMC5883L)
from .complementary_filter import ComplementaryFilter

class SensorConsole(object):
    def __init__(self):
        self.gps = GPS()
        # self.bmp = BMP180()
        self.gyro = GY521()
        self.compass = HMC5883L()

    @asyncio.coroutine
    def readSensorData(self, copter):
        print("this is inside readSensorData",  copter.state)
        # lat, long = self.gps.getLatLLong()
        # copter.initialStateSpace.lat = lat
        # copter.initialStateSpace.long = long
        # copter.initialStateSpace.altitude = self.bmp.getAltitude()
        # roll, pitch = self.gyro.getRollPitch()
        # copter.initialStateSpace.roll = roll
        # copter.initialStateSpace.pitch = pitch
        # copter.initialStateSpace.yaw = self.compass.getYaw()

        while copter.state is not 'stopped':
            # lat, long = yield from self.gps.getLatLong()
            # copter.currentStateSpace.lat = lat
            # copter.currentStateSpace.long = long
            # copter.currentStateSpace.altitude = yield from self.bmp.getAltitude()
            gyro_out, acc_out =  self.gyro.raw_data()

            pitch, roll = ComplementaryFilter(gyro_out, acc_out, 
                                copter.currentStateSpace.pitch,  copter.currentStateSpace.roll)

            copter.currentStateSpace.roll = roll
            copter.currentStateSpace.pitch = pitch
            copter.currentStateSpace.yaw = self.compass.getYaw()
            # if copter.log:
            #     self.copter.currentStateSpace.log()
            yield from asyncio.sleep(0.01)  # interval should be same as dt in ComplementaryFilter(0.01 sec)
        
        print("stopping readSensorData coroutine:")
