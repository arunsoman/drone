
import asyncio

class WirelessReader(object):
    def __init__(self):

    @asyncio.coroutine
    def getData(self):
        with open('/proc/net/wireless', 'r') as f:
            for aLine in f:
            yield from aLine