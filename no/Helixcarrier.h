#ifndef Helixcarrier_h
#define Helixcarrier_h

#include "Arduino.h"
#include "Motor.h"

class Helixcarrier
{
private:
	Motor motor1;
	Motor motor2;
	Motor motor3;
	Motor motor4;
	Servo* servo;;
public:
	Helixcarrier(Servo* servo);
	~Helixcarrier();
	void setStep(float av1,float av2,float av3,float av4);	
};
#endif