import asyncio

from .sensor.sensorconsole import SensorConsole
from .model.statespace import StateSpace
from .model.thrustManager import ThrustManager
from .model.copterDynamics import  get_transformation

class HeliCarrier(object):
    def __init__(self):
        self.length = .25  # meters
        self.liftConstant = 1
        self.currentStateSpace = StateSpace()
        self.initialStateSpace = StateSpace()
        self.thrustManager = ThrustManager()
        self.sensorConsole = SensorConsole()
        self.state = 'stopped'
        self.log = False

    def start(self):
        (asyncio.get_event_loop()
            .create_task(self.sensorConsole.readSensorData(self)))
        self.thrustManager.startEngine()
        self.state = "started"

    def stop(self):
        self.thrustManager.stopEngine()
        self.state = "stopped"

    def getCurrentLocation(self):
        return self.currentStateSpace

    def moveTo(self, point):
        r, t = get_transformation(
            self.currentStateSpace.getVector(self.currentLocation),
            self.initialPlan.getVector(point)
        )
        roll, pitch, yaw = getRollPitchYaw(r)

    def getCorrectionVolt(self, roll, pitch, yaw):
        volt1, volt2, volt3, volt4 = 0
        # TODO
        return volt1, volt2, volt3, volt4

    def _manual(self, s1, s2, s3, s4):
        self.log = True
        print (self.currentStateSpace)
        print (s1, s2, s3, s4)
        self.thrustManager._manual(s1, s2, s3, s4)
        print (self.currentStateSpace)
