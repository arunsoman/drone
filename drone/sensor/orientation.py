import asyncio
from drone.sensor import MPU6050
import math

class Orientation(object):

    def __init__(self):
        self.mpu = MPU6050()
        self.mpu.dmpInitialize()
        self.mpu.setDMPEnabled(True)
        self.ypr = None
        # get expected DMP packet size for later comparison
        self.packetSize = self.mpu.dmpGetFIFOPacketSize()
        self.shutdown = False

    @asyncio.coroutine
    def start_recording(self):
        while not self.shutdown:
            # Get INT_STATUS byte
            mpuIntStatus = self.mpu.getIntStatus()

            if mpuIntStatus >= 2: # check for DMP data ready interrupt (this should happen frequently)
                # get current FIFO count
                fifoCount = self.mpu.getFIFOCount()

                # check for overflow (this should never happen unless our code is too inefficient)
                if fifoCount == 1024:
                    # reset so we can continue cleanly
                    self.mpu.resetFIFO()
                    # print('FIFO overflow!')


                # wait for correct available data length, should be a VERY short wait
                fifoCount = self.mpu.getFIFOCount()
                while fifoCount < self.packetSize:
                    yield from asyncio.sleep(0.001)
                    fifoCount = self.mpu.getFIFOCount()

                result = self.mpu.getFIFOBytes(self.packetSize)
                q = self.mpu.dmpGetQuaternion(result)
                g = self.mpu.dmpGetGravity(q)
                self.ypr = self.mpu.dmpGetYawPitchRoll(q, g)
                # rad2deg = (180 / math.pi)
                # print(self.ypr['yaw']*rad2deg,self.ypr['pitch']*rad2deg,self.ypr['roll']*rad2deg)


                # track FIFO count here in case there is > 1 packet available
                # (this lets us immediately read more without waiting for an interrupt)
                fifoCount -= self.packetSize

            else:
                # print("ignoring..", fd)
                pass
            yield from asyncio.sleep(0.1)

    def getRawData(self):
        rad2deg = (180 / math.pi)
        return self.ypr['yaw']*rad2deg,self.ypr['pitch']*rad2deg,self.ypr['roll']*rad2deg