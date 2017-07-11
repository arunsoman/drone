import sys
import os
import asyncio


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


from sensor import GY521

imu = GY521()



@asyncio.coroutine
def  read_cor():
    gyro_out, acc_out = imu.raw_data()
    # print (acc_out, gyro_out)
    return acc_out, gyro_out


from fusion_async import Fusion



f = Fusion(read_cor)

end = False
def stopfunc():
    return end


@asyncio.coroutine
def wait():
        global end
        yield from asyncio.sleep(10)
        end = True
        asyncio.get_event_loop().create_task(f.start(slow_platform=True))

asyncio.get_event_loop().create_task(f.calibrate(stopfunc))
asyncio.get_event_loop().create_task(wait())



@asyncio.coroutine
def print_val():
    while 1:
        print("q: %s roll: %s pitch %s yaw: %s" % (f.q, f.roll, f.pitch, f.heading ))
        yield from asyncio.sleep(1)


asyncio.get_event_loop().create_task(print_val())
asyncio.get_event_loop().run_forever()