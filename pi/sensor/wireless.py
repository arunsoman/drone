
import asyncio

class WirelessReader(object):
    def __init__(self):

    @asyncio.coroutine
    def getData(self):
        with open('workfile', 'r') as f:
            for aLine in f:
            yield from aLine