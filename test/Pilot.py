import os
import sys
sys.path.append((os.path.dirname(os.path.dirname(__file__))))

import time
import asyncio

from drone.helicarrier import HeliCarrier



@asyncio.coroutine
def launch():
    copter = HeliCarrier()
    print("ok")
    copter.start()
    s1 = s2 = s3 = s4 = 10
    s = [s1, s2, s3, s4]
    copter._manual(s1, s2, s3, s4)
    time.sleep(4)
    yield from testSingle(copter, s1, s1 + 20, 0, s)
    yield from testSingle(copter, s1, s1 + 20, 1, s)
    yield from testDouble(copter, s1, s1 + 20, 0, 1, s)
    yield from testDouble(copter, s1, s1 + 20, 2, 3, s)


@asyncio.coroutine
def testSingle(copter, initial, final, index, s):
    for i in range(initial, final):
        s[index] = i
        copter._manual(s[0], s[1],  s[2], s[3])
        yield from asyncio.sleep(4)



@asyncio.coroutine
def testDouble(copter, initial, final, index1, index2, s):
    for i in range(initial, final):
        s[index1] = i
        s[index2] = i
        copter._manual(s[0], s[1],  s[2], s[3])
        yield from asyncio.sleep(4)



loop = asyncio.get_event_loop()
loop.run_until_complete(launch())