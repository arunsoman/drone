import serial
import os, time
from decimal import *


try:
    # for the sake of testing.
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
except:
    pass  


class GPS(object):
    def __init__(self):
        self.port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)

    def __find(str, ch):
        for i, ltr in enumerate(str):
            if ltr == ch:
                yield i

    def getLatLong(self):
        fd = ''
        while fd.find('$GPRMC') > 0:
            fd = ''
            ck = 0
            while ck  <= 50:
                rcv = self.port.read(10)
                fd = fd + rcv
                ck = ck + 1

        # print fd
        if '$GPRMC' in fd:
            ps = fd.find('$GPRMC')
            dif = len(fd) - ps
            # print dif
            if dif > 50:
                data = fd[ps:(ps + 50)]
                print(data)
                p = list(self.__find(data, ","))
                lat = data[(p[2] + 1):p[3]]
                lon = data[(p[4] + 1):p[5]]

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

                print(s1)
                print(s2)
                return s1,s2
