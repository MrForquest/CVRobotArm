#include <Servo.h>

#define numFingers 5

byte codeMode;

byte servoPins[numFingers] = {4, 2, 3, 5, 6};
byte startValues[numFingers] = {40, 75, 25, 10, 90};
byte endValues[numFingers] = {100, 135, 95, 90, 150};

Servo handServos[numFingers];

void setup() {
  Serial.begin(9600); // Инициализация Serial - порта
  for (int i = 0; i < numFingers; i++) {
    handServos[i].attach(servoPins[i]);
    handServos[i].write(startValues[i]);
  }
}

void loop() {
  if (Serial.available() > 0)
  {
    codeMode = Serial.read();
    Serial.println(codeMode);
    if (codeMode == 1) // 1 - Enable - включить
    {
      //myservo.write(100);
    }
    else if (codeMode == 2) // 2 - Disable - выключить
    {
      //myservo.write(10);
    }
    else if (codeMode == 3) // 3 - массив на все 5 серв
    {
      byte fingersValues[numFingers];

      Serial.readBytes(fingersValues, numFingers);
      
      for (int i = 0; i < numFingers; i++) {
        if (fingersValues[i] == 1) {
          handServos[i].write(endValues[i]);
        }
        else {
          handServos[i].write(startValues[i]);
        }
      }
      //Serial.write(fingersValues[0]);
      //Serial.println(fingersValues[0]);
    }

  }
}
