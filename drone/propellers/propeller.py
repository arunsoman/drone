

#http://m-selig.ae.illinois.edu/props/propDB.html

class Propeller(object):
    def __init__(self,pitch, diameter):
        self.D = diameter
        self.rho = 1.225
        self.pitch = pitch

    def liftForce(self, w):
        return Ct * self.D**4 * self.rho * w**2

    def torque(self, W):
        return Cp * self.D**5 * self.rho * W**2