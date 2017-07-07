def motorTorque(current, mR, kv, omega):
    return (current * mR + kv * omega)


def force(current, mR, kv, omega):
    return motorTorque(current, mR, kv, omega) / omega


def mass(current, mR, kv, omega):
    return force(current, mR, kv, omega) * 9.8


def omega(rpm):
    return rpm * 2 * 3.14 / 60


def magic():
    # https://www.rcgroups.com/forums/showthread.php?1086319-ESC-PWM-value-More-RPMs
    # http://community.silabs.com/t5/8-bit-MCU/relationship-between-motor-speed-and-PWM-frequency/td-p/83577
    #Fpolesw = 6*(poleNumber) / 2*rpm
    return


def calibrateESC(motors):
    print('***Disconnect ESC power')
    print('***then press ENTER')
    res = raw_input()
    try:
        for aMotor in motors:
            aMotor.start()
            aMotor.setW(100)

        print('***Connect ESC Power')
        print('***Wait beep-beep')
        res = raw_input()
        for aMotor in motors:
            aMotor.start()
            aMotor.setW(0)
        print('***Wait N beep for battery cell')
        print('***Wait beeeeeep for ready')
        print('***then press ENTER')
        res = raw_input()

        for aMotor in motors:
            aMotor.start()
            aMotor.setW(10)
        res = raw_input()
    finally:
        # shut down cleanly
        for aMotor in motors:
            aMotor.stop()
