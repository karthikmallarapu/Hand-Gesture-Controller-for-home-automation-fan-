#include <Servo.h>

Servo servo;
int fanPin = 3;  // Pin for controlling the fan through the transistor

void setup() {
  servo.attach(9);         // Servo connected to pin 9
  pinMode(fanPin, OUTPUT); // Fan control pin
  digitalWrite(fanPin, LOW);  // Ensure the fan is off initially
  Serial.begin(9600); 
  pinMode(13,OUTPUT);     // Serial communication
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');

    // Fan speed control
    if (command.startsWith("F")) {
      int fanSpeed = command.substring(1).toInt();

      if (fanSpeed == 0) 
      {
        digitalWrite(13,LOW);
        // If fanSpeed is 0, turn off the fan by setting the pin LOW
        digitalWrite(fanPin, LOW); 
      }
       else
        {
        // Otherwise, adjust the fan speed with PWM (map 0-100 to 0-255)
        analogWrite(fanPin, map(fanSpeed, 0, 100, 0, 255));
        digitalWrite(13,HIGH);
      }
    }

    // Servo direction control
    if (command.startsWith("S")) {
      char direction = command[1];
      if (direction == 'L') 
      {
        servo.write(0);  // Turn left
      } 
      else if (direction == 'R') 
      {
        servo.write(180);  // Turn right
      }
       else 
      {
        servo.write(90);  // Center
      }
    }
  }
}
