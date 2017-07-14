import asyncio

import time

import math

import numpy as np
from calibraxis import Calibraxis

dt = 2
g = 9.8


class Anemometer(object):
    def __init__(self,statespace,gps,mpu):
        self.speed = 0
        self.mpu = mpu
        self.statespace = statespace
        gps.register(self.reset)
        pass

    def reset(self, speed):
        self.speed = speed



    def update(self):
        self.mpu.get_accel_data()

    @asyncio.coroutine
    def start_calculation(self):
        t = time.time()
        c = Calibraxis()
        points=[]
        for _ in range(0):
            print("calibrating",points)
            ax,ay,az = self.mpu.get_accel_data(True)
            points.append([ax,ay,az])
            # print (ax,ay,az)
            ax1 = ax + g * math.sin( self.statespace.roll)
            ay1 = ay +  g * math.sin( self.statespace.pitch)
            az1 = az +  g* (math.cos( self.statespace.roll) * math.cos( self.statespace.pitch))
            # print (ax1,ay1,az1)
            # print (self.statespace.roll,self.statespace.pitch,self.statespace.yaw)
            t1=time.time();
            self.statespace.vx =ax1
            self.statespace.vy = ay1
            self.statespace.vz = az1
            t=t1;
            yield from asyncio.sleep(dt)
            print (self.statespace.vx,self.statespace.vy,self.statespace.vz)
            now = time.time()
            # print("error in time", dt - (t-now))


      #  print(points)
       # c.add_points(points)

        #c  .calibrate_accelerometer()

        while True:
            ax,ay,az = self.mpu.get_accel_data()

            # print ("acce",ax,ay,az)
           # ax,ay,az=c.apply([ax,ay,az])
           # print ("aftercalibrate",ax,ay,az)
            print ("roll: ",self.statespace.roll,"pitch",self.statespace.pitch)
            print("acc",ax,ay,az)
            ax1 = ax -  g * math.sin( math.radians(self.statespace.pitch))
            ay1 = ay -  g * math.sin( math.radians(self.statespace.roll))
            az1 = az +  g* (math.cos(math.radians(self.statespace.roll))
                            * math.cos(math.radians( self.statespace.pitch)))
            print (ax1,ay1,az1)
            print("")
            # print (self.statespace.roll,self.statespace.pitch,self.statespace.yaw)
            t1=time.time();
            self.statespace.vx =ax1

            self.statespace.vy =ay1
            self.statespace.vz =az1
            t=t1;
            yield from asyncio.sleep(3)
            # print (self.statespace.vx,self.statespace.vy,self.statespace.vz)
            now = time.time()
            # print("error in time", dt - (t-now))


