import serial
import os
import time
import asyncio

from decimal import *
from geopy.distance import vincenty

# for the sake of testing.
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)


class GPS(object):
    def __init__(self):
        self.port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
        self.latlong = [0,0,0,time.time()]
        self.degrees = None

       

    def __find(self, str, ch):
        for i, ltr in enumerate(str):
            if ltr == ch:
                yield i

    @asyncio.coroutine
    def start_recording(self):
        while True:
            fd = ''
            while fd.find('$GPRMC') == -1:
                fd = ''
                ck = 0
                while ck <= 50:
                    rcv = self.port.read(10)
                    yield from asyncio.sleep(0)
                    fd = fd +  rcv.decode('ascii', errors="ignore")
                    ck = ck + 1

            # print(fd)
            if '$GPRMC' in fd :
                ps = fd.find('$GPRMC')
                dif = len(fd) - ps
                print(fd)
                if dif > 50:
                    data = fd[ps:(ps + 50)]
                    # print(data)
                    p = list(self.__find(data, ","))
                    # print("xxxxx", p)
                    lat = data[(p[2] + 1):p[3]]
                    lon = data[(p[4] + 1):p[5]]

                    try:
                        # print("hooo")
                        s1 = lat[2:len(lat)]
                        s1 = Decimal(s1)
                        s1 = s1 / 60
                        s11 = int(lat[0:2])
                        s1 = s11 + s1

                        s2 = lon[3:len(lon)]
                        s2 = Decimal(s2)
                        s2 = s2 / 60
                        s22 = int(lon[0:3])
                        s2 = s22 + s2
                        current = [float(s1), float(s2),0,time.time()]
                        velocity = vincenty(self.latlong[0:1], current[0:1]).meters/(current[3] - self.latlong[3])
                        current[3] = velocity
                        self.latlong = current
                    except Exception as oops:
                        print(oops)
                yield from asyncio.sleep(0.1)

if __name__ == '__main__':
    print(GPS().getLatLong())
