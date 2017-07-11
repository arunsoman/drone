import threading


def threadify(fn):
    def func(*args, **kwargs):
        return threading.Thread(target=fn, args=args, kwargs=kwargs)
    return func


class Motor(object):
    def __init__(self, name, pin, kv=1000, WMin=0, WMax=100, debug=True, simulation=False):
        self.dragCoeff = 1.5
        self.liftConst = 1
        self.omega = 0
        self.name = name
        self.powered = True
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
            print("simulation ****")
            self.simulation = True

    def attachPropeller(self,propeller):
        self.propeller=propeller

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
            print("******** setting pwm",PW)
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
            print ("powered is :",self.powered)
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

    def getThrustGiven(self, rpm, v):
        c1 = 4.392399*(10**-8)*rpm*(self.propeller.D**3.5)
        c2 = (4.23333*(10**-4)*rpm*self.propeller.pitch) - v
        c3 = self.propeller.pitch**(0.5)
        return c1*c2/c3

    def getRpmGiven(self, thrust, v):
        a = 4.392399*(10**-8)*(self.propeller.D**3.5)*4.23333*(10**-4)*(self.propeller.pitch**0.5)
        b = 4.392399*(10**-8)*(self.propeller.D**3.5)/(self.propeller.pitch**0.5)
        c = -thrust
        return -b+((((b**2)-(4*a*c))**(0.5))/(2*a))

    def __repr__(self):
        return "<%s(%s) @ %s>" % (self.name, self.__pin, self.__W)
