Helixcarrier c = new Helixcarrier();
void setup()                    // run once, when the sketch starts
{
  Serial.begin(9600);           // set up Serial library at 9600 bps
  
  Serial.println("Hello world!");  // prints hello with ending line break 


}

void loop()                       // run over and over again
{
  c.setStep(40, 40, 40, 40);                                // do nothing!
}