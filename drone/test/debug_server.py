import asyncio
import websockets
import random
import json


DATA_UPLINK_INTERVAL = 0.5
WS_SERVER_PORT = 8765


class DebugServer(object):

    def __init__(self, coptor):
        """ 
        :param coptor: HeliCarrier instance
        """
        self.coptor = coptor

    def consolidate_data(self):
        data = ("{" + self.coptor.currentStateSpace.serialize() + ','
                    + self.coptor.thrustManager.serialize() + "}")
        # print("data", data)
        return data

    @asyncio.coroutine
    def instruction_handler(self, websocket):
        while True:
            message = yield from websocket.recv()
            try:
                (instr, *args) = message.split(',')
                if instr == 'start':
                    self.coptor.start()
                elif instr == 'stop':
                    self.coptor.stop()
                elif instr == 'yaw':
                    self.coptor.thrustManager.yaw(args[0], int(args[1]))
                elif instr == 'pitch':
                    self.coptor.thrustManager.pitch(args[0], int(args[1]))
                elif instr == 'roll':
                    self.coptor.thrustManager.roll(args[0], int(args[1]))
                elif instr == 'altitude':
                    self.coptor.thrustManager.altitude(args[0], int(args[1]))
                elif instr == 'mannual':
                    self.coptor.thrustManager._manual(*map(int, args))
                else:
                    print(" **** unknown instruction", instr)
            except Exception as oops:
                print("error in instruction", oops)

    @asyncio.coroutine
    def uplink_handler(self, websocket):
        while True:
            message = self.consolidate_data()
            yield from websocket.send(message)
            yield from asyncio.sleep(DATA_UPLINK_INTERVAL)

    @asyncio.coroutine
    def handler(self, websocket, path):
        print(" **** debug client connected", websocket.remote_address)
        consumer_task = asyncio.get_event_loop().create_task(
            self.instruction_handler(websocket))
        producer_task = asyncio.get_event_loop().create_task(self.uplink_handler(websocket))
        done, pending = yield from asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:
            task.cancel()
        print(" **** debug client disconnected", websocket.remote_address)

    def start(self):
        start_server = websockets.serve(
            self.handler, '0.0.0.0', WS_SERVER_PORT)
        print(" **** starting debug socket server...")
        asyncio.get_event_loop().create_task(start_server)
