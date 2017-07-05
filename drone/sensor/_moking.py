import random


class SMBus(object):
    def __init__(self, *k, **w):
        pass

    def read_byte_data(self, bus, addr):
        return random.randint(0x00, 0xFF)

    def write_byte_data(self, bus, addr, val):
        pass
