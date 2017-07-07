from drone.motors import motor, MotorFactory


class ThrustManager(object):
    def __init__(self):
        # ''''
        # 1 ---------- 2
        # 3 -----------4
        # '''
        # '''cw'''
        self.__motor1 = MotorFactory.getA2212_13t('m1', 17, simulation=False)
        self.__motor3 = MotorFactory.getA2212_13t('m3', 25, simulation=False)
        # '''ccw'''
        self.__motor2 = MotorFactory.getA2212_13t('m2', 18, simulation=False)
        self.__motor4 = MotorFactory.getA2212_13t('m4', 22, simulation=False)
        self.__motors = [self.__motor1, self.__motor2,
                         self.__motor3, self.__motor4, ]

    def __execute(self, tasks):
        for i in tasks:
            i.start()
        for i in tasks:
            i.join()

    def startEngine(self):
        tasks = [
            self.__motor1.start(),
            self.__motor2.start(),
            self.__motor3.start(),
            self.__motor4.start(),
        ]
        self.__execute(tasks)

    def stopEngine(self):
        tasks = [
            self.__motor1.stop(),
            self.__motor2.stop(),
            self.__motor3.stop(),
            self.__motor4.stop(),
        ]
        self.__execute(tasks)

    def roll(self, direction, step):
        tasks = [
            self.__motor2.setW(step),
            self.__motor4.setW(step)
        ] if direction is 'left' else[
            self.__motor1.setW(step),
            self.__motor3.setW(step)
        ]
        self.__execute(tasks)

    def pitch(self, direction, step):
        tasks = [
            self.__motor2.setW(step),
            self.__motor1.setW(step)
        ] if direction is 'up' else[
            self.__motor4.setW(step),
            self.__motor3.setW(step)
        ]
        self.__execute(tasks)

    def yaw(self, direction, step):
        tasks = [
            self.__motor4.setW(step),
            self.__motor1.setW(step)
        ] if direction is 'cw' else[
            self.__motor2.setW(step),
            self.__motor3.setW(step)
        ]
        self.__execute(tasks)

    def altitude(self, direction, step):
        tasks = [
            self.__motor4.increaseW(step),
            self.__motor3.increaseW(step),
            self.__motor2.increaseW(step),
            self.__motor1.increaseW(step),
        ] if direction is 'assend' else[
            self.__motor4.decreaseW(step),
            self.__motor3.decreaseW(step),
            self.__motor2.decreaseW(step),
            self.__motor1.decreaseW(step),
        ]
        self.__execute(tasks)

    def _manual(self, s1, s2, s3, s4):
        tasks = [
            self.__motor4.increaseW(s1),
            self.__motor3.increaseW(s2),
            self.__motor2.increaseW(s3),
            self.__motor1.increaseW(s4),
        ]
        self.__execute(tasks)

    def totalTorque(self):
        torque = 0
        for motor in self.__motors:
            torque += motor.torque()
        return torque

    def torqueComponents(self, length, liftConstant):
        lk = length * liftConstant
        return [
            lk * (-self.__motor2.torqueSq() + self.__motor4.torqueSq()),
            lk * (-self.__motor1.torqueSq() + self.__motor3.torqueSq()),
            self.totalTorque()
        ]

    def print_motors(self):
        print("\t".join(map(repr, self.__motors)))

    def serialize(self):
        """
        return a dict of pwm of each motor.
        """
        return "m1:%s,m2:%s,m1:%s,m2:%s" % (self.__motor1.get_w(),
                                            self.__motor2.get_w(),
                                            self.__motor2.get_w(),
                                            self.__motor3.get_w())
