#include "Helixcarrier.h"

Helixcarrier:Helixcarrier(){
	Servo = new Servo()
	motor1 = new Motor(2 servo);
	motor2 = new Motor(6 servo);
	motor3 = new Motor(8 servo);
	motor4 = new Motor(4 servo);
}

void Helixcarrier:setStep(float av1,float av2,float av3,float av4){
	motor4.setStep(av1);
motor2.setStep(av2);
motor3.setStep(av3);
motor4.setStep(av4);

}