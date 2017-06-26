#ifndef Motor_h
#define Motor_h

#include "Arduino.h"
#include <Servo.h>

class Motor{
private:
	int pin;
	Servo* servo;

public:
	Motor(int pin, Servo* servo)
	void setPWM(int step);
}

#endif