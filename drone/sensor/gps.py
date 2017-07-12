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
        self.course = 0
        self.degrees = None
        self.shutdown = True
        self.speed = 0
        self.prev_time = time.time()

    def __decode(self, str):
        return str.decode('ascii',errors='ignore')

    def raw_data(self):
        return self.lat,self.long,self.speed, self.course

    @asyncio.coroutine
    def start_recording(self):
        print("inside gps")
        self.port.write(b"$PMTK397,0.2*3F\r\n")
        self.port.write(b"$PMTK397,0.2*3F\r\n")
        self.port.write(b"$PMTK220,100*2F\r\n")
        while self.shutdown:
            fd = self.port.readline()
            yield from asyncio.sleep(0)
            if fd.startswith(b'$GPRMC'):
                # print("*******", fd)
                result = fd.split(b',')
                if result[2] == b'A':
                    try:
                        self.lat = int(result[3][:2]) + float(result[3][2:].decode('ascii',errors='ignore'))/60
                        self.long = int(result[5][:3]) + float(result[5][3:].decode('ascii',errors='ignore')) / 60
                    except Exception as oops:
                        print(oops)
                    # now = time.time()
                    # dist = vincenty((self.lat, self.long),(lat,lon)).meters / (current[3] - self.latlong[3])
                    # current[3] = velocity
                    # self.latlong = current
                    # print("latlongg..", self.lat, self.long)
            if fd.startswith(b'$GPVTG'):
                result = fd.split(b',')
                try:
                    self.course = float(result[1].decode('ascii',errors='ignore'))
                    self.speed = float(result[7].decode('ascii',errors='ignore'))
                except Exception as oops:
                    print(oops)
            else:
                # print("ignoring..", fd)
                pass
            yield from asyncio.sleep(0.1)


if __name__ == '__main__':
    print(GPS().getLatLong())
