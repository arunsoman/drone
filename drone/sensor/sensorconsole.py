import asyncio

from drone.sensor import GPS, BMP180, HMC5883L, Orientation, Anemometer

class SensorConsole(object):
    def __init__(self,copter):
        self.copter=copter
        self.gps = GPS()

        self.bmp = BMP180()
        self.orientation = Orientation()
        self.anemomter = Anemometer(self.copter.currentStateSpace, self.gps, self.orientation.mpu)
        # self.gyro = GY521()
        # self.compass = HMC5883L()
        # self.ahrs = MadgwickAHRS()
        asyncio.get_event_loop().create_task(self.gps.start_recording())
        asyncio.get_event_loop().create_task(self.bmp.start_recording())
        asyncio.get_event_loop().create_task(self.anemomter.start_calculation())
        asyncio.get_event_loop().create_task(self.orientation.start_recording())

    @asyncio.coroutine
    def readSensorData(self):
        print("this is inside readSensorData")
        self.updateStateSpace(self.copter.initialStateSpace)

        while self.copter.state is not 'stopped':
            self.updateStateSpace(self.copter.currentStateSpace)
            yield from asyncio.sleep(0)  # interval should be same as dt in ComplementaryFilter(0.01 sec)
        
        print(" stopping readSensorData coroutine:")

    def updateStateSpace(self, sp):
        sp.lat, sp.long = self.gps.raw_data()
        sp.altitude = self.bmp.getAltitude()
        # gyro_out, acc_out = self.gyro.raw_data()
        # magnetometer = self.compass.raw_data()
        magnetometer = None
        #print("***********", self.ahrs.get_roll_pitch_yaw_heading(gyro_out, acc_out, magnetometer))
        # sp.roll, sp.pitch, sp.yaw = self.ahrs.get_roll_pitch_yaw_heading(gyro_out, acc_out, magnetometer)
        sp.yaw, sp.pitch, sp.roll = self.orientation.getRawData()
    # def updateStateSpace(self, sp):
