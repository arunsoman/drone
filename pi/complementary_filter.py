#!/usr/bin/python

import numpy as np
import asyncio
import time
import smbus
import math


ACCELEROMETER_SENSITIVITY = 8192.0
GYROSCOPE_SENSITIVITY = 65.536
dt = 0.01
M_PI = 3.14159265359


def ComplementaryFilter(gyrData, accData, pitch, roll):

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
    from sensor import GY521
    import sys
    pitch = 0
    roll = 0
    i = 0;
    mpu = GY521()
    while True:
        gyro_out, acc_out,  = mpu.raw_data()
        pitch, roll = ComplementaryFilter(gyro_out,acc_out, pitch, roll)
        # sys.stderr.write("Acc: %s \t Gyr: %s                     \r" %(acc_out_scale, gyro_out_scale))
        i += 1
        if not (i % 10):
            sys.stderr.write(
                "pitch: %s \t roll: %s                     \r" % (pitch, roll))
            sys.stderr.flush()
            i = 0

        
        # print ("gyro_out: ", gyro_out)
        # print ("acc_out: ", acc_out)
        # print ("gyro_out_scale: ", gyro_out_scale)
        # print ("acc_out_scale: ", acc_out_scale)
        # print ("getRotation", getRotation(gyro_out_scale,"X"),getRotation(gyro_out_scale,"Y"),getRotation(gyro_out_scale,"Z"))
        time.sleep(dt)
