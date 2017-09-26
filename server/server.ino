/*
PINOUT
8  - VCC #2 
9  - TRIG 1
10 - ECHO 1
11 - TRIG 2
12 - ECHO 2
*/
#include "Ultrasonic.h"

// We need to make our own library for improving triggering and resolution
//Ultrasonic u1(9, 10);
Ultrasonic u1(11, 12, 6500);
int count = 0;

void setup()
{
	Serial.begin(9600);
  pinMode(13, OUTPUT);
  pinMode(8, OUTPUT);
  digitalWrite(8, LOW);
}

void loop()
{
  int dat1 = u1.distanceRead();
  //int dat2 = u2.distanceRead();
	if (Serial.available() > 0) {
    //Do nothing  
	}
  if (count < 1000) {
    digitalWrite(13, HIGH);
    Serial.println(dat1);
    count += 1;
  }
  else{
    count = 0;
    digitalWrite(13, LOW);
    sleep(1000);
  }

  //Serial.print(" ");
  //Serial.println(dat2);
  
}
