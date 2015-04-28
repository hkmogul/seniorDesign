int gate = 9;
int incomingByte = 0;
int ledPin = 13;
//Switch activator is the ASCII '2' or the 
//int 50 and it is used to start 
//and stop the cameras.
String content = "";
char character;
int tempo; // beats per second
float milliTempo; // beats per millisecond
int state = 0; // 0 for not recording, 1 for recording
void setup()
{
  Serial.begin(9600);
  pinMode(gate, OUTPUT);
}

void loop()
{
//  if (Serial.available() > 0) {
//    incomingByte = Serial.read();
//    //Serial.print("Available\n");
//    //Serial.print(incomingByte);
//    
//    if (incomingByte == 'S') {
//      analogWrite(gate, 255);
//      delay(200);
//    
//      analogWrite(gate, 0);
//      delay(1000);
//      //Serial.print("Switch Pushed\n");

      while(Serial.available()){
        character = Serial.read();
        content.concat(character);
      }
      // check if this turns on the cameras- S for START
      if(content.length() > 0 && content.charAt(0) == 'S' && state == 0){
        // parse tempo from 
        state = 1;
        tempo = content.substring(1).toInt();
        analogWrite(gate, 255);
        delay(200);
        analogWrite(gate, 0);
        content ="";
      }
      //check if we're turning off the camera- T for TERMINATE
      else if(content.length() > 0 && content.charAt(0) == 'T' && state == 1){
        state = 0;
        analogWrite(gate, 255);
        delay(200);
        analogWrite(gate, 0);
        content = "";
      }
      // else, this is a garbage message and we should ignore it and reset
      else{
        content = "";
      }
      // metronome control
      if (state == 1){
        // time in seconds % tempo == 0 means flash
        if( (int(millis()*1000) % tempo) == 0){
          digitalWrite(ledPin, HIGH);
          delay(10); // so it doesnt immediately turn off 
        }
        else{
          digitalWrite(ledPin, LOW);
        }
      }
      // make sure metronome is off if not recording
      else{
        digitalWrite(ledPin, LOW);
      }

}
