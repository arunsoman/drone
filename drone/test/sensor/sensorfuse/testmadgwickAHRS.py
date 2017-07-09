import sensor.sensorfuse.madgwickAHRS as m
import unittest

from sensor import GPS, BMP180, GY521, HMC5883L


class testMadgwickAHRS(unittest.TestCase):
    def __init__(self):
        self.gps = GPS()
        self.bmp = BMP180()
        self.gyro = GY521()
        self.compass = HMC5883L()
        self.ahrs = m.MadgwickAHRS()

    def test_with_loop(self):
        gyroscope, accelerometer =self.gyro.raw_data()
        roll, pitch, yaw, heading = m.get_roll_pitch_yaw_heading(gyroscope, accelerometer, self.compass.get_raw_data)
        print(roll, pitch, yaw, heading)