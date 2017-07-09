import asyncio

from sensor import (GPS, BMP180, GY521, HMC5883L)
from sensor.sensorfuse.madgwickAHRS import MadgwickAHRS


class SensorConsole(object):
    def __init__(self):
        self.gps = GPS()
        self.bmp = BMP180()
        self.gyro = GY521()
        self.compass = HMC5883L()
        self.ahrs = MadgwickAHRS()
        print(self.gps.start_recording())
        asyncio.get_event_loop().create_task(self.gps.start_recording())

    @asyncio.coroutine
    def readSensorData(self, copter):
        print("this is inside readSensorData",  copter.state)
        self.__updateStateSpace(copter.initialStateSpace)

        while copter.state is not 'stopped':
            self.__updateStateSpace(copter.currentStateSpace)
            yield from asyncio.sleep(0.01)  # interval should be same as dt in ComplementaryFilter(0.01 sec)
        
        print("stopping readSensorData coroutine:")

    def __updateStateSpace(self, sp):
        sp.lat, sp.long, sp.speed, _ = self.gps.getLatLLong()
        sp.altitude = yield from self.bmp.getAltitude()
        gyro_out, acc_out = self.gyro.raw_data()
        magnetometer = self.compass.getData()
        sp.roll,sp.pitch,sp.yaw, sp.heading = self.ahrs.get_roll_pitch_yaw(gyro_out, acc_out, magnetometer)