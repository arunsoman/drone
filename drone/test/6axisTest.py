from calibraxis import Calibraxis
import time
import math
import mpu6050
import numpy as np

# Sensor initialization
mpu = mpu6050.MPU6050()
mpu.dmpInitialize()
mpu.setDMPEnabled(True)

# get expected DMP packet size for later comparison
packetSize = mpu.dmpGetFIFOPacketSize()
array = np.array()

a = Calibraxis()
g = Calibraxis()

apoints = np.array([[0, 0, 0]])
gpoints = np.array([[0, 0, 0]])

for _ in range(1,100):
    # Get INT_STATUS byte
    mpuIntStatus = mpu.getIntStatus()

    if mpuIntStatus >= 2: # check for DMP data ready interrupt (this should happen frequently)
        # get current FIFO count
        fifoCount = mpu.getFIFOCount()

        # check for overflow (this should never happen unless our code is too inefficient)
        if fifoCount == 1024:
            # reset so we can continue cleanly
            mpu.resetFIFO()
            print('FIFO overflow!')


        # wait for correct available data length, should be a VERY short wait
        fifoCount = mpu.getFIFOCount()
        while fifoCount < packetSize:
            fifoCount = mpu.getFIFOCount()

        result = mpu.getFIFOBytes(packetSize)
        q = mpu.dmpGetQuaternion(result)
        g = mpu.dmpGetGravity(q)
        ypr = mpu.dmpGetYawPitchRoll(q, g)

        # rad2deg = (180 / math.pi)
        gpoints.append([ypr['yaw'] * rad2deg,ypr['pitch']*rad2deg,ypr['roll']*rad2deg])

        # track FIFO count here in case there is > 1 packet available
        # (this lets us immediately read more without waiting for an interrupt)
        fifoCount -= packetSize

a.add_points(apoints)
print("Points",apoints)
# Run the calibration parameter optimization.
a.calibrate_accelerometer()
self.a=a


while True:
    acc_out = np.array([ypr['yaw'] * rad2deg,ypr['pitch']*rad2deg,ypr['roll']*rad2deg
    ])
    acc_out=self.a.apply(acc_out)
    print("A",acc_out)