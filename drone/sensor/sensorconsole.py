import asyncio

from drone.sensor import GPS, BMP180, GY521, HMC5883L
from drone.sensor.sensorfuse.madgwickAHRS import MadgwickAHRS


class SensorConsole(object):
    def __init__(self):
        self.gps = GPS()
        self.bmp = BMP180()
        self.gyro = GY521()
        # self.compass = HMC5883L()
        self.ahrs = MadgwickAHRS()
        asyncio.get_event_loop().create_task(self.gps.start_recording())

    @asyncio.coroutine
    def readSensorData(self, copter):
        print("this is inside readSensorData")
        self.updateStateSpace(copter.initialStateSpace)

        while copter.state is not 'stopped':
            self.updateStateSpace(copter.currentStateSpace)
            yield from asyncio.sleep(0)  # interval should be same as dt in ComplementaryFilter(0.01 sec)
        
        print(" stopping readSensorData coroutine:")

    def updateStateSpace(self, sp):
        sp.lat, sp.long, sp.speed, sp.course = self.gps.raw_data()
        sp.altitude = self.bmp.getAltitude()
        gyro_out, acc_out = self.gyro.raw_data()
        # magnetometer = self.compass.raw_data()
        magnetometer = None
        #print("***********", self.ahrs.get_roll_pitch_yaw_heading(gyro_out, acc_out, magnetometer))
        sp.roll, sp.pitch, sp.yaw = self.ahrs.get_roll_pitch_yaw_heading(gyro_out, acc_out, magnetometer)

    # def updateStateSpace(self, sp):
