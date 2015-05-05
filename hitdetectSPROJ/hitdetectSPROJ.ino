/*
New and improved code for Team ColDRUMbia position sensing drum pad
Hilary Mogul & Shahrod Khalkali
*/
const static int sensePins[9]={A0, A1, A2, A3, A4, A5, A6, A7, A8};

const static String xPositions[9] = {"-1","00","01","-1","00","01","-1","00","01"};
const static String yPositions[9] = {"01","01","01","00","00","00","-1","-1","-1"};

static int prevVal[9] = {0,0,0,0,0,0,0,0,0};
 
static int vel;
float elapsedTime = 1;
float currentTime;

int currVal;
//int hits;
long slope;
int diff;
// Thresholds go here

int sensorThresh = 250;
int slopeThresh = -1;
//int diffThresh = -60;
int diffThresh= 80;
// possibly check for below threshold && local minima to make sure we 
/*
If hit detected, return 1-127 velocity, 0 for non hit- dont forget to load
*/
String val2vel(int val){
  // first convert to 1-127
  float slp = 0.5;
  int vel = 127-int(slp*val);
  String s;
  if(vel<10){
    s= "00"+String(vel);
    return s;
  }
  else if(vel<100){
    s = "0"+String(vel);
    return s;
  }
  else{
    s = String(vel);
    return s;
  }
}

int localMin(int pin, int prevVal){
    currVal = analogRead(pin);
    if(currVal < prevVal){
      // continue checking
      return localMin(pin, currVal);
    }
    else{
      return prevVal;
    }
}

int hitCheck(int pin){
  // DETECTION ALGORITHM GOES HERE
  currVal = analogRead(sensePins[pin]);
//  diff = currVal - prevVal[pin];
  diff = abs(currVal-prevVal[pin]);
  elapsedTime = micros() - currentTime;
  slope = (currVal - prevVal[pin])/elapsedTime;
  
  if(currVal < sensorThresh && diff > diffThresh && currVal < prevVal[pin]/* && slope < slopeThresh */){
//    hits++;
//    Serial.println(slope);
//    Serial.println(diff);
    prevVal[pin] = currVal;
//    Serial.println(currVal);
    return localMin(pin, currVal);
//      return currVal;
  }
  prevVal[pin] = currVal;
  currentTime = micros();
  return 0;
}


void setup() {
  // put your setup code here, to run once:
  Serial.begin(19200);
//  sensePins = {sensor0, sensor1, sensor2, sensor3, sensor4, sensor5, sensor6, sensor7, sensor8};
//  xPositions = {-1,0,1,-1,0,1,-1,0,1};
//  yPositions = {1,1,1,0,0,0,-1,-1,-1};
  currentTime = micros();
//  hits = 0;
  for(int i  = 0; i <9; i++){
     prevVal[i] = analogRead(sensePins[i]);
  } 
}

void loop() {
  // put your main code here, to run repeatedly:
  for(int i = 0; i < 9; i++){
    if((vel = hitCheck(i)) != 0){
      String message = xPositions[i] + yPositions[i] + val2vel(vel);
      Serial.println("");
      Serial.println(message);
//      Serial.println(hits);
      for(int i  = 0; i <9; i++){
         prevVal[i] = analogRead(sensePins[i]);
      } 
      delay(10);
    }
    
  }
}
