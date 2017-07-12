import asyncio

class Anemometer(object):
    def __init__(self,gps,mpu):
        self.speed = 0
        self.mpu = mpu
        gps.register(self.update())
        pass

    def reset(self, speed):
        self.speed = speed



    def update(self):
        self.mpu.get_accel_data()

    @asyncio.coroutine
    def start_calculation(self):
        while True:
            print(self.mpu.get_accel_data())
            yield from asyncio.sleep(0.5)

