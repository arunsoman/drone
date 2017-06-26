#include "Motor.h"

Motor:Motor(int pin, Servo* servo){
	pin = pin;
	servo = servo;
}

Motor:setStep(int step){
	*servo.write(step);
}
