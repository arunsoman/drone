def motorTorque(current, mR,kv,omega):
    return  (current*mR + kv*omega)

def force(current, mR,kv,omega):
    return motorTorque(current, mR,kv,omega)/omega

def mass(current, mR,kv,omega):
    return force(current, mR,kv,omega)*9.8

def omega(rpm):
    return rpm*2*3.14/60

def magic():
    #https://www.rcgroups.com/forums/showthread.php?1086319-ESC-PWM-value-More-RPMs
    #http://community.silabs.com/t5/8-bit-MCU/relationship-between-motor-speed-and-PWM-frequency/td-p/83577
    #Fpolesw = 6*(poleNumber) / 2*rpm