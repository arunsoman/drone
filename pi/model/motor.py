

class Motor(object):
    def __init__(self):
        self.dragCoeff = 1.5
        self.liftConst = 1
        self.omega = 0
        self.resistence = .1

    def torque(self):
        return self.dragCoeff*(self.omega**2)

    def thrust(self):
        return self.liftConst*(self.omega**2)

    def getOmegaSq(self):
        return self.omega**2

    def setVoltage(self, volt):
        self.omega = self.getOmegaGiven(volt)

    def getVoltageGiven(self, omega):
        return

    def getOmegaGiven(self, volt):
        return