#!/usr/bin/python

import numpy as np
import asyncio
import time
import smbus
import math

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))


def getRotation(point, axis):
    if axis is 'X':
        radians = math.atan2(point[1], dist(point[0], point[2]))
        return math.degrees(radians)
    if axis is 'Y':
        radians = math.atan2(point[0], dist(point[1], point[2]))
        return -math.degrees(radians)
    if axis is 'Z':
        radians = math.atan2(point[2], dist(point[0], point[1]))
        return -math.degrees(radians)
    
bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)

def extractData():
    gyro_out = np.array([
        read_word_2c(0x43),
        read_word_2c(0x45),
        read_word_2c(0x47)])

    acc_out = np.array([
        read_word_2c(0x3b),
        read_word_2c(0x3d),
        read_word_2c(0x3f)
    ])

    gyro_out_scale = 131 / gyro_out
    acc_out_scale = 16384 / acc_out

    return gyro_out, gyro_out_scale, acc_out, acc_out_scale

while True:
    gyro_out, gyro_out_scale, acc_out, acc_out_scale = extractData()

    print ("gyro_out: ", gyro_out)
    print ("acc_out: ", acc_out)
    print ("gyro_out_scale: ", gyro_out_scale)
    print ("acc_out_scale: ", acc_out_scale)
    print ("getRotation", getRotation(gyro_out_scale,"X"),getRotation(gyro_out_scale,"Y"),getRotation(gyro_out_scale,"Z"))
    time.sleep(2)
