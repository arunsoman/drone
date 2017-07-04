from helicarrier import HeliCarrier
import time

def launch():
    copter = HeliCarrier()
    copter.start()
    s1 = s2 = s3 = s4 = 10
    s=[s1,s2,s3,s4]
    copter.__manual(s1,s2,s3,s4)
    time.sleep(4)
    testSingle(copter,s1, s1+20, 0,s)
    testSingle(copter,s1, s1+20, 1,s)
    testDouble(copter,s1, s1+20, 0, 1,s)
    testDouble(copter,s1, s1+20, 2, 3,s)

def testSingle(copter, initial, final, index, s):
    for i in range(initial,final):
        s[index] = i
        copter.__manual(s[0], s[1],  s[2], s[3])
        time.sleep(4)
        copter.h

def testDouble(copter, initial, final, index1, index2, s):
    for i in range(initial,final):
        s[index1] = i
        s[index2] = i
        copter.__manual(s[0], s[1],  s[2], s[3])
        time.sleep(4)