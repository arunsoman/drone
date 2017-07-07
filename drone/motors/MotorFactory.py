from motors.motor import Motor


def getA2212_13t(name, pin, simulation=True):
    motor = Motor(name, pin, kv=1000,simulation=simulation)
    motor.__MaxEfficiency=	80##%
    motor.__MaxEfficiencyCurrent=	4#-10A(>75%)
    motor.__NoLoadCurrent=	0.5#A@10V
    motor.__Resistance=	0.090#ohms
    motor.__MaxCurrent=	4#Afor60S
    motor.__MaxWatts=	150#W
    motor.__Weight=	52.7#g/1.86oz
    motor.__torque = lambda (omega): (motor.__MaxCurrent * motor.__Resistance + motor.__kv * omega)
    motor.__force=lambda (omega): motor.__torque(omega)/omega
    motor.__liftCapacity =lambda (omega): (motor.__force(omega))*9.8
    #motor.__Size=	28mmdiax28mmbelllength
    #motor.__ShaftDiameter=	3.2mm
    #motor.__Poles=	14
    #motor.__ModelWeight=	300-800g
    return motor