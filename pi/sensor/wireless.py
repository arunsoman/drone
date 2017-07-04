
import asyncio

class WirelessReader(object):
    def __init__(self):
        pass

    def getData(self):
        with open('/proc/net/wireless', 'r') as f:
            return parse_signal_level(f.read())