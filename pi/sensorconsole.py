import asyncio

from sensor import (GPS,BMP180,GY521,HMC5883L)

class SensorConsole(object):
    def __init__(self):
        self.gps = GPS()
        self.bmp = BMP180()
        self.gyro = GY521()
        self.compass = HMC5883L()
    

    @asyncio.coroutine
    def readSensorData(self, copter ):
        lat, long = self.gps.getLatLong()
        copter.initialStateSpace.lat = lat
        copter.initialStateSpace.long = long
        copter.initialStateSpace.altitude = self.bmp.getAltitude()
        roll, pitch = self.gyro.getRollPitch()
        copter.initialStateSpace.roll = roll
        copter.initialStateSpace.pitch = pitch
        copter.initialStateSpace.yaw = self.compass.getYaw()

        while copter.state is not 'stopped':
            lat, long = self.gps.getLatLong()
            copter.currentStateSpacev.lat = lat
            copter.currentStateSpacev.long = long
            copter.currentStateSpacev.altitude = self.bmp.getAltitude()
            roll, pitch = self.gyro.getRollPitch()
            copter.currentStateSpacev.roll = roll
            copter.currentStateSpacev.pitch = pitch
            copter.currentStateSpacev.yaw = self.compass.getYaw()
            if copter.log:
                self.copter.currentStateSpacev.log()

