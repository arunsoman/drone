from helicarrier import HeliCarrier
import time

def launch():
    copter = HeliCarrier()
    copter.start()
    s1 = s2 = s3 = s4 = 10
    copter.__manual(s1,s2,s3,s4)
    time.sleep(4)
    
