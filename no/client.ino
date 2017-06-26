#include <pt.h>

Sensor sensor = new Sensor();
static struct pt pt1;

static int commandReader(struct pt *pt) { 
    PT_BEGIN(pt); 
    while(1) {
    	bool command =commandFromPi();
    	if(command==true){
    		processCommand();
    	}           
        PT_WAIT_UNTIL(pt, !command ); 
        sendSensorDataToPI(); 
    } 
    PT_END(pt);
}

bool commandFromPi(){
	return Serial.available()>0;
}

void sendSensorDataToPI(){
	String stat = sensor.getData();
	Serial.write(stat);
}

void processCommand(){
	String command = Serial.readString();
}

Helixcarrier c = new Helixcarrier();
void setup()
{
  Serial.begin(9600); 
  PT_INIT(pt1);

}

void loop()
{
  commandReader(pt1);
  c.setStep(40, 40, 40, 40);//this should happen in processCommand
}