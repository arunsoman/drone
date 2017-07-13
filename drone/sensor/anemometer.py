import asyncio

import time

import math
dt = 0.5
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
        while True:
            ax,ay,az = self.mpu.get_accel_data()

            print (ax,ay,az)
            ax1 = ax + g * math.sin( self.statespace.roll)
            ay1 = ay +  g * math.sin( self.statespace.pitch)
            az1 = az +  g* (math.cos( self.statespace.roll) + math.cos( self.statespace.pitch))
            self.statespace.vx += (ax1 * dt)
            self.statespace.vy += (ay1 * dt)
            self.statespace.vz += (az1 * dt)
            yield from asyncio.sleep(dt)
            print (self.statespace.vx,self.statespace.vy,self.statespace.vz)
            now = time.time()
            print("error in time", dt - (t-now))
            t = now

