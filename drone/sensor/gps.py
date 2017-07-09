import serial
import os
import time
import asyncio

from geopy.distance import vincenty

# for the sake of testing.
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)


class GPS(object):
    def __init__(self):
        self.port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
        self.lat = 0
        self.long = 0
        self.velocity = 0
        self.prev_time = time.time()

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
                    p = list(self.__find(data, ","))
                    lat = data[(p[2] + 1):p[3]]
                    lon = data[(p[4] + 1):p[5]]

                    try:
                        s1 =  float(lat[2:])/ 60   # minutes
                        s11 = int(lat[:2])         # degrees
                        self.lat = s11 + s1

                        s2 = float(lon[3:])/60
                        s22 = int(lon[:3])
                        self.long = s22 + s2

                        dist = vincenty((self.lat, self.long), (s1, s2)).meters
                        now = time.time()

                        print("distance covered = ",dist, "time taken = ", now - self.prev_time)
                        self.velocity = dist/(now - self.prev_time)
                        self.prev_time = now

                    except Exception as oops:
                        print(oops)
                yield from asyncio.sleep(0.01)

if __name__ == '__main__':
    print(GPS().getLatLong())
