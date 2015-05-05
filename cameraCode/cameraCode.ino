#include <elapsedMillis.h>

elapsedMillis metroTime;
elapsedMillis timeElapsed;
int gate = 9;
//int incomingByte = 0;
int ledPin = 13;
//Switch activator is the ASCII '2' or the 
//int 50 and it is used to start 
//and stop the cameras.
String content = "";
char character;
long tempo; // beats per second
long temp;
static long period; // milliseconds per beat
//long timeBeat; // elapsed time since last beat
//int prevTime;
int state = 0; // 0 for not recording, 1 for recording
void setup()
{
  Serial.begin(9600);
  pinMode(gate, OUTPUT);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
  analogWrite(gate, 0);
  state = 0;
  period = 5*1000; // only blink every 10 seconds
//  while(!Serial){ // wait until serial connection is made
//    ;
//  }
//  timeBeat = 0;
}

void loop()
{
    while(!Serial){
      ;
    }
    delay(20);

      // read two bytes and get temporary interval.  if it passes some threshold (idk) its good
      if(Serial.available()){
        if(Serial.read() =='W'){
          int i = Serial.parseInt();
          int j = Serial.parseInt();
          Serial.println(i);
          Serial.println(j);
          temp = 255*i+j;
          analogWrite(gate, 255);
          delay(200);
          analogWrite(gate, 0);
          period = temp;
          timeElapsed=0;
          metroTime = 0;
          Serial.println("NEW TEMPO");
          Serial.println(period);
        }
//          if( temp > 100)
      }
      if( timeElapsed > period){
        digitalWrite(ledPin, HIGH);
        Serial.println("1 ");
//        Serial.print(timeElapsed);
        metroTime = 0;
        timeElapsed = 0;
        delay(10); // so it doesnt immediately turn off 
      }
      else{
        digitalWrite(ledPin, LOW);
        Serial.println("0 ");
//        Serial.print(timeElapsed);

      }
//      Serial.println(timeElapsed);
//      Serial.println("--");
//      Serial.println(period);
      

}
