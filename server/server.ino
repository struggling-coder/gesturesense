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
Ultrasonic u1(9, 10, 5000);
Ultrasonic u2(11, 12, 5000);
Ultrasonic u3(4, 7, 5000);
int count = 0;

void setup()
{
	Serial.begin(9600);
  pinMode(13, OUTPUT);
  pinMode(8, OUTPUT);
  digitalWrite(8, HIGH);
  pinMode(2, OUTPUT);
  digitalWrite(2, HIGH);
}

void loop()
{
  int dat1 =  u1.distanceRead();
  int dat2 =  u2.distanceRead();
	int dat3 =  u3.distanceRead();
  
	if (Serial.available() > 0) {
  }

  if (count < 1000) { 
    digitalWrite(13, HIGH); 
    Serial.print(dat1); 
    Serial.print(" ");
    Serial.print(dat2);
    Serial.print(" ");
    Serial.println(dat3);
    count += 1; 
  } 
  else{ 
    count = 0; 
    digitalWrite(13, LOW); 
    delay(1); 
  } 
 
  
}
