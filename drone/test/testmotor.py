#solenerotech 2013.07.31
#solenero.tech@gmail.com
#solenerotech.wordpress.com

class motor(object):
    """Manages the currect Angular rotation
    Implements the IO interface using the RPIO lib
    __init_(self, mId, pin, kv=1000, RPMMin=1, RPMMax=100, debug=True, simulation=True):
    More info on RPIO in http://pythonhosted.org/RPIO/index.html"""

    __mId = 0
    __pin = 17
    __kv = 1000    #not used
    __RPM = 0     #given in %
    __RPMMin = 1    #given in %
    __RPMMax = 100    #given in %
    __RPMEquil = 50    # RPM that equilibry the gravity,in%
    simulation = True    #used to skip the IO interface.useful if develping not in rpi
    debug = True

    def __init__(self, mId, pin, kv=1000, RPMMin=1, RPMMax=100, debug=True, simulation=True):
        self.__mId = mId
        self.__pin = pin
        self.__kv = kv
        if RPMMin < 0:
            RPMMin = 0
        self.__RPMMin = RPMMin
        if RPMMax > 100:
            RPMMax = 100
        self.__RPMMax = RPMMax
        self.debug = debug
        self.simulation = simulation
        self.__RPM = 0
        self.__RPMEquil = 50
        if self.simulation:
            return

        from RPIO import PWM
        self.__IO = PWM.Servo()

    def stop(self):
        "Sets RPM=0"
        self.setRPM(0)
        if not self.simulation:
            self.__IO.stop_servo(self.__pin)

    def configure(self, kv=1000, RPMMin=1, RPMMax=100):
        "configures kv,rpmmin,rpmmax"
        self.__kv = kv
        if RPMMin < 0:
            RPMMin = 0
        self.__RPMMin = RPMMin
        if RPMMax > 100:
            RPMMax = 100
        self.__RPMMax = RPMMax

    def setRPMEquil(self):
        "Sets current RPM% =RPMEquil"
        self.__RPMEquil = self.__RPM

    def getRPMEquil(self):
        "returns current RPM% =RPMEquil"
        self.__RPM = self.__RPMEquil

    def increaseRPM(self, step=1):
        "increases RPM% for the motor"

        self.__RPM = self.__RPM + step
        self.setRPM(self.__RPM)

    def decreaseRPM(self, step=1):
        "decreases RPM% for the motor"

        self.__RPM = self.__RPM - step
        self.setRPM(self.__RPM)

    def getRPM(self):
        "retuns current RPM%"
        return self.__RPM

    def setRPM(self, RPM):
        "Checks RPM% is between limits than sets it"
        self.__RPM = RPM
        if self.__RPM < self.__RPMMin:
            self.__RPM = self.__RPMMin
        if self.__RPM > self.__RPMMax:
            self.__RPM = self.__RPMMax
        if self.debug :
            print ('M' + str(self.__mId) + ' RPM %: ' + str(self.__RPM))
        if not self.simulation:
            PW=(1 + (self.__RPM / 100)) * 1000
            # Set servo to xxx us
            self.__IO.set_servo(self.__pin,PW)
            return
        return
M = motor('m1',4,simulation=False)
M.configure()
M.setRPM(100)
while 1:
   pass