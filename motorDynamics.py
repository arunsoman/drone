import math as m
row = 1.225; #kg/m3 air density
kv = 5700;
'''
If you use SI units (Nm/A for KTKT, V/(rad/s) for KeKe), then 
KT=KeKT=Ke for DC motors and permanent-magnet synchronous motors (aka "brushless DC")

pick a motor with a KTKT and back-emf constant such that the supply voltage you have 
available is well-matched with the back-emf at your maximum speed. You usually want back-emf 
voltage to be 80-95% of the supply voltage, but the exact number depends on the load torque and 
the IR drop in the motor at that operating point.

If you pick a KT=KeKT=Ke too high, you'll run out of voltage and won't be able to achieve the speed you need.
If you pick a KT=KeKT=Ke too low, the current needed to achieve the torque you need will be higher than necessary.
'''
#Propeller constant = Propeller pitch / 1853.2

def computeTorque(KT, I, I0):
    return KT(I - I0)

def toAngularVelocity(rpm):
    return 2*3.14*rpm/60

def get_cube_root(num):
    return num ** (1. / 3)

#def motor():
def getVoltageWhen(current, resistence, av):
    return current*resistence + kv*av

def getPower(current, resistence, av):
    return current*getVoltageWhen(current,resistence,av)

def getThrust(current, resistence, av, A):
    return get_cube_root(getPower(current,resistence,av)*2*row*A)

def getArea(current, resistence, av, mg):
    return (mg**3)/(getPower(current,resistence,av)*2*row)

#return getThrust

def du():
    mas = 1
    f = mas*9.8
    print f
    print getThrust(10, .5, toAngularVelocity(5000),.5)
    print getThrust(10, .5, toAngularVelocity(1000),.5)
    print getThrust(10, .5, toAngularVelocity(5000),1)
    print getThrust(10, .5, toAngularVelocity(5000),2)
    print getArea(10, .5, toAngularVelocity(5000),f)
du()import math as m
row = 1.225; #kg/m3 air density
kv = 5700;
'''
If you use SI units (Nm/A for KTKT, V/(rad/s) for KeKe), then 
KT=KeKT=Ke for DC motors and permanent-magnet synchronous motors (aka "brushless DC")

pick a motor with a KTKT and back-emf constant such that the supply voltage you have 
available is well-matched with the back-emf at your maximum speed. You usually want back-emf 
voltage to be 80-95% of the supply voltage, but the exact number depends on the load torque and 
the IR drop in the motor at that operating point.

If you pick a KT=KeKT=Ke too high, you'll run out of voltage and won't be able to achieve the speed you need.
If you pick a KT=KeKT=Ke too low, the current needed to achieve the torque you need will be higher than necessary.
'''

def computeTorque(KT, I, I0):
    return KT(I - I0)

def toAngularVelocity(rpm):
    return 2*3.14*rpm/60

def get_cube_root(num):
    return num ** (1. / 3)

#def motor():
def getVoltageWhen(current, resistence, av):
    return current*resistence + kv*av

def getPower(current, resistence, av):
    return current*getVoltageWhen(current,resistence,av)

def getThrust(current, resistence, av, A):
    return get_cube_root(getPower(current,resistence,av)*2*row*A)

def getArea(current, resistence, av, mg):
    return (mg**3)/(getPower(current,resistence,av)*2*row)

#return getThrust

def du():
    mas = 1
    f = mas*9.8
    print f
    print getThrust(10, .5, toAngularVelocity(5000),.5)
    print getThrust(10, .5, toAngularVelocity(1000),.5)
    print getThrust(10, .5, toAngularVelocity(5000),1)
    print getThrust(10, .5, toAngularVelocity(5000),2)
    print getArea(10, .5, toAngularVelocity(5000),f)
du()
