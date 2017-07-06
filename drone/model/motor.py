import threading


def threadify(fn):
    def func(*args, **kwargs):
        return threading.Thread(target=fn, args=args, kwargs=kwargs)
    return func


class Motor(object):
    def __init__(self, name, pin, kv=1000, WMin=0, WMax=100, debug=True, simulation=True):
        self.dragCoeff = 1.5
        self.liftConst = 1
        self.omega = 0
        self.resistence = .1
        self.name = name
        self.powered = False
        self.simulation = simulation
        self.__pin = pin
        self.__kv = kv
        self.__WMin = WMin if WMin >= 0 else 0
        self.__WMax = WMax if WMin <= 100 else 100
        # self.setDebug(debug)
        self.__W = self.__WMin
        self.__Wh = 10
        try:
            from RPIO import PWM
            self.__IO = PWM.Servo()
        except ImportError:
            self.simulation = True

    def _setw(self, W):
        "Checks W% is between limits than sets it"
        PW = 0
        self.__W = W
        if self.__W < self.__WMin:
            self.__W = self.__WMin
        if self.__W > self.__WMax:
            self.__W = self.__WMax
        PW = (1000 + (self.__W) * 10)
        # Set servo to xxx us
        if self.powered:
            self.__IO.set_servo(self.__pin, PW)

    def get_w(self):
        return self.__W
    
    @threadify
    def start(self):
        "Run the procedure to init the PWM"
        if not self.simulation:
            try:
                from RPIO import PWM
                self.__IO = PWM.Servo()
                self.powered = True
                # TODO Decide How to manage the WMax < 100
                # to keep anyhow the throttle range 0-100
            except ImportError:
                self.simulation = True
                self.powered = False

    @threadify
    def stop(self):
        "Stop PWM signal"
        self._setw(0)
        if self.powered:
            self.__IO.stop_servo(self.__pin)
            self.powered = False

    @threadify
    def setW(self, W):
        self._setw(W)

    @threadify
    def increaseW(self, step=1):
        self._setw(self.__W + step)

    @threadify
    def decreaseW(self, step=1):
        self._setw(self.__W - step)

    def torque(self):
        return self.dragCoeff * (self.omega**2)

    def thrust(self):
        return self.liftConst * (self.omega**2)

    def getOmegaSq(self):
        return self.omega**2

    def setVoltage(self, volt):
        self.omega = self.getOmegaGiven(volt)

    def getVoltageGiven(self, omega):
        return

    def getOmegaGiven(self, volt):
        return

    def __repr__(self):
        return "<%s(%s) @ %s>" % (self.name, self.__pin, self.__W)
