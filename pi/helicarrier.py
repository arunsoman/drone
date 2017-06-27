import asyncio
import pinointerface as ch
from sensor.gy85 import GY85


@asyncio.coroutine
def readFromGyro():
    gyro = GY85()
    while True:
        yield from gyro.extractData()

def caliberate(alignment):
	return [20,20,20]

def start():	
	ch.connect()
	alignment = ch.receive()
	ch.send(caliberate(alignment))
	ch.disconnect()

start()