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
        self.degrees = None
        self.shutdown = True
        self.last_time = time.time()
        self.callbacks = []
        self.activated = False

    def __decode(self, str):
        return str.decode('ascii',errors='ignore')

    def register(self, callback):
        self.callbacks.append(callback)

    def raw_data(self):
        return self.lat,self.long

    @asyncio.coroutine
    def start_recording(self):
        print("inside gps")
        self.port.write(b"$PMTK397,0*23F\r\n")
        self.port.write(b"$PMTK397,0.2*3F\r\n")
        self.port.write(b"$PMTK220,100*2F\r\n")
        while self.shutdown:
            fd = self.port.readline()

            if fd.startswith(b'$GPRMC'):
                # print("*******", fd)
                result = fd.split(b',')
                if result[2] == b'A':
                    self.activated = True
                    now = time.time()
                    try:
                        lat = int(result[3][:2]) + float(result[3][2:].decode('ascii',errors='ignore'))/60
                        lon = int(result[5][:3]) + float(result[5][3:].decode('ascii',errors='ignore')) / 60
                        if self.long != lon or self.lat != lat:
                            dist = vincenty((self.lat, self.long),(lat,lon)).meters
                            speed = dist/ (now - self.last_time)
                            print("speed from distance", speed)
                            for cb in self.callbacks:
                                cb(speed)
                        self.lat, self.long,self.last_time = lat, lon, now
                    except Exception as oops:
                        print(oops)
                else:
                    self.activated = False
                    # now = time.time()
                    # dist = vincenty((self.lat, self.long),(lat,lon)).meters / (current[3] - self.latlong[3])
                    # current[3] = velocity
                    # self.latlong = current
                    # print("latlongg..", self.lat, self.long)
            if fd.startswith(b'$GPVTG'):
                if self.activated:
                    print(fd)
                    result = fd.split(b',')
                    try:
                        # self.course = float(result[1].decode('ascii',errors='ignore'))
                        gps_speed = float(result[7].decode('ascii',errors='ignore'))
                        print("speed from gps", gps_speed)
                        for cb in self.callbacks:
                            cb(gps_speed)

                    except Exception as oops:
                        print(oops)
            else:
                # print("ignoring..", fd)
                pass
            yield from asyncio.sleep(0.1)


if __name__ == '__main__':
    print(GPS().getLatLong())
