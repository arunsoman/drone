#!/usr/bin/python

import numpy as np
import asyncio
import time
import smbus
import math

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

class GY85(object):
    def __call__(self, address = 0x68, **kwargs):
        self.bus = smbus.SMBus(1)  # or bus = smbus.SMBus(1) for Revision 2 boards
        self.address = address
        # Now wake the 6050 up as it starts in sleep mode
        self.bus.write_byte_data(address, power_mgmt_1, 0)

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


    def getRotation(self,point, axis):
        if axis is 'X':
            radians = math.atan2(point[1], self.dist(point[0], point[2]))
            return math.degrees(radians)
        if axis is 'Y':
            radians = math.atan2(point[0], self.dist(point[1], point[2]))
            return -math.degrees(radians)
        if axis is 'Z':
            radians = math.atan2(point[2], self.dist(point[0], point[1]))
            return -math.degrees(radians)

    def extractData(self):
        gyro_out = np.array([
            self.read_word_2c(0x43),
            self.read_word_2c(0x45),
            self.read_word_2c(0x47)])

        acc_out = np.array([
            self.read_word_2c(0x3b),
            self.read_word_2c(0x3d),
            self.read_word_2c(0x3f)
        ])

        gyro_out_scale = 131 / gyro_out
        acc_out_scale = 16384 / acc_out

        return gyro_out, gyro_out_scale, acc_out, acc_out_scale

def test():
    gyro = GY85()
    while range(0,10):
        gyro_out, gyro_out_scale, acc_out, acc_out_scale = gyro.extractData()

        print ("gyro_out: ", gyro_out)
        print ("acc_out: ", acc_out)
        print ("gyro_out_scale: ", gyro_out_scale)
        print ("acc_out_scale: ", acc_out_scale)
        print (
        "getRotation", getRotation(gyro_out_scale, "X"), getRotation(gyro_out_scale, "Y"), getRotation(gyro_out_scale, "Z"))
        time.sleep(2)