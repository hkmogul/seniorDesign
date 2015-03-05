/*
  Analog Input
 Demonstrates analog input by reading an analog sensor on analog pin 0 and
 turning on and off a light emitting diode(LED)  connected to digital pin 13.
 The amount of time the LED will be on and off depends on
 the value obtained by analogRead().

 The circuit:
 * Potentiometer attached to analog input 0
 * center pin of the potentiometer to the analog pin
 * one side pin (either one) to ground
 * the other side pin to +5V
 * LED anode (long leg) attached to digital output 13
 * LED cathode (short leg) attached to ground

 * Note: because most Arduinos have a built-in LED attached
 to pin 13 on the board, the LED is optional.


 Created by David Cuartielles
 modified 30 Aug 2011
 By Tom Igoe

 This example code is in the public domain.

 http://arduino.cc/en/Tutorial/AnalogInput

 */

int sensorPin = A0;    // select the input pin for the potentiometer
int sensorPin2 = A1;
int ledPin = 13;      // select the pin for the LED
int sensorValue = 0;  // variable to store the value coming from the sensor
int sensorValue2 = 0;
int threshold = 750;
int sensorPrev = 0;
int sensorPrev2 = 0;
int thresh2 = 100;

void setup() {
  // declare the ledPin as an OUTPUT:
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // read the value from the sensor:
  digitalWrite(ledPin, LOW);
  sensorValue = analogRead(sensorPin);
  sensorValue2 = analogRead(sensorPin2);
  // turn the ledPin on
  if(sensorValue < threshold && abs(sensorPrev-sensorValue) > thresh2){
    digitalWrite(ledPin, HIGH);
    Serial.println("Hit detected at sensor 1");
    Serial.println(sensorValue);
    Serial.println(millis());
    Serial.println("----");

  }
  
  else if(sensorValue2 < threshold && abs(sensorPrev2-sensorValue2) > thresh2){
    digitalWrite(ledPin, HIGH);
    Serial.println("Hit detected at sensor 2");
    Serial.println(sensorValue2);
    Serial.println(millis());
    Serial.println("----");
  }
  sensorPrev = sensorValue;
  sensorPrev2 = sensorValue2;
}
