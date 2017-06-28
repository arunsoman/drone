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


ACCELEROMETER_SENSITIVITY = 8192.0
GYROSCOPE_SENSITIVITY = 65.536
dt = 0.01
M_PI = 3.14159265359


def ComplementaryFilter(accData, gyrData, pitch, roll):

    pitchAcc = 0.0
    rollAcc = 0.0
    # Integrate the gyroscope data -> int(angularSpeed) = angle
    pitch += (gyrData[0] / GYROSCOPE_SENSITIVITY) * dt  # Angle around the X-axis
    roll -= (gyrData[1] / GYROSCOPE_SENSITIVITY) *  dt  # Angle around the Y-axis

    # Compensate for drift with accelerometer data if !bullshit
    # Sensitivity = -2 to 2 G at 16Bit -> 2G = 32768 && 0.5G = 8192
    forceMagnitudeApprox = abs(accData[0]) + abs(accData[1]) + abs(accData[2])
    if (forceMagnitudeApprox > 8192 and forceMagnitudeApprox < 32768):
            # Turning around the X axis results in a vector on the Y-axis
        pitchAcc = math.atan2(accData[1], accData[2]) * 180 / M_PI
        pitch = pitch * 0.98 + pitchAcc * 0.02

        # Turning around the Y axis results in a vector on the X-axis
        rollAcc = math.atan2(accData[0], accData[2]) * 180 / M_PI
        roll = roll * 0.98 + rollAcc * 0.02
    return pitch, roll


if __name__ == '__main__':
    import sys
    pitch = 0
    roll = 0
    while True:
        gyro_out, gyro_out_scale, acc_out, acc_out_scale = extractData()
        pitch, roll = ComplementaryFilter(acc_out, gyro_out, pitch, roll)
        # sys.stderr.write("Acc: %s \t Gyr: %s                     \r" %(acc_out_scale, gyro_out_scale))
        sys.stderr.write(
            "pitch: %s \t roll: %s                     \r" % (pitch, roll))
        sys.stderr.flush()
        # print ("gyro_out: ", gyro_out)
        # print ("acc_out: ", acc_out)
        # print ("gyro_out_scale: ", gyro_out_scale)
        # print ("acc_out_scale: ", acc_out_scale)
        # print ("getRotation", getRotation(gyro_out_scale,"X"),getRotation(gyro_out_scale,"Y"),getRotation(gyro_out_scale,"Z"))
        time.sleep(.1)
