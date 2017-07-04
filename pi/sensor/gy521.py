#!/usr/bin/python

import numpy as np
import asyncio
import time
import math


try:
    # for the sake of testing.
    import smbus
except:
    from . import _moking as smbus

class GY521(object):

    # Power management registers
    power_mgmt_1 = 0x6b
    power_mgmt_2 = 0x6c

    def __init__(self, port=1, address=0x68):
        self.address = address     # This is the address value read via the i2cdetect command
        self.bus = smbus.SMBus(port)  #bus = smbus.SMBus(1) for Revision 2 boards
        
        # Now wake the 6050 up as it starts in sleep mode
        self.bus.write_byte_data(address, GY521.power_mgmt_1, 0)
    
    def __call__(self):
        return self.raw_data()

    def raw_data(self):
        gyro_out = np.array([
            self.read_word_2c(0x43),
            self.read_word_2c(0x45),
            self.read_word_2c(0x47)])

        acc_out = np.array([
            self.read_word_2c(0x3b),
            self.read_word_2c(0x3d),
            self.read_word_2c(0x3f)
        ])
        return gyro_out, acc_out

    def read_byte(self,adr):
        return self.bus.read_byte_data(self.address, adr)

    def read_word(self,adr):
        high = self.bus.read_byte_data(self.address, adr)
        low = self.bus.read_byte_data(self.address, adr + 1)
        val = (high << 8) + low
        return val

    def read_word_2c(self,adr):
        val = self.read_word(adr)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

    def dist(self, a, b):
        return math.sqrt((a * a) + (b * b))

    def get_rotation(self,point, axis):
        if axis is 'X':
            radians = math.atan2(point[1], self.dist(point[0], point[2]))
            return math.degrees(radians)
        if axis is 'Y':
            radians = math.atan2(point[0], self.dist(point[1], point[2]))
            return -math.degrees(radians)
        if axis is 'Z':
            radians = math.atan2(point[2], self.dist(point[0], point[1]))
            return -math.degrees(radians)

    def extract_data(self):
        gyro_out,acc_out = self.raw_data()
        # scaled data: do we realy need this?
        gyro_out_scale = gyro_out / 131
        acc_out_scale =  acc_out /  16384

        return gyro_out, gyro_out_scale, acc_out, acc_out_scale

    def getRollPitch(self):
        #//TODO
        return 0,0

if __name__ == '__main__':
    # test
    imu = GY521()
    for i in range(10):
            gyro_out, gyro_out_scale, acc_out, acc_out_scale = imu.extract_data()

            print ("gyro_out: ", gyro_out)
            print ("acc_out: ", acc_out)
            print ("gyro_out_scale: ", gyro_out_scale)
            print ("acc_out_scale: ", acc_out_scale)
            print (
            "getRotation", imu.get_rotation(gyro_out_scale, "X"), imu.get_rotation(gyro_out_scale, "Y"), imu.get_rotation(gyro_out_scale, "Z"))
            break
            time.sleep(2)

