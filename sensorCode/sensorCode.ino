/*
New and improved code for Team ColDRUMbia position sensing drum pad
Hilary Mogul & Shahrod Khalkali
*/
const static int sensePins[9]={A0, A1, A2, A3, A4, A5, A6, A7, A8};

const static int xPositions[9] = {-1,0,1,-1,0,1,-1,0,1};
const static int yPositions[9] = {1,1,1,0,0,0,-1,-1,-1};
static int prevValues[9] = {0,0,0,0,0,0,0,0,0};
 
static int vel;
float elapsedTime = 1;
// Thresholds go here



// possibly check for below threshold && local minima to make sure we 
/*
If hit detected, return 1-127 velocity, 0 for non hit- dont forget to load
*/
int hitCheck(int pin, int prev){
  // DETECTION ALGORITHM GOES HERE
  return 0;  
}
void setup() {
  // put your setup code here, to run once:
  Serial.begin(19200);
//  sensePins = {sensor0, sensor1, sensor2, sensor3, sensor4, sensor5, sensor6, sensor7, sensor8};
//  xPositions = {-1,0,1,-1,0,1,-1,0,1};
//  yPositions = {1,1,1,0,0,0,-1,-1,-1};
  for(int i  = 0; i <9; i++){
     prevValues[i] = analogRead(sensePins[i]);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  for(int i = 0; i < 9; i++){
    if((vel = hitCheck(sensePins[i], prevValues[i])) != 0){
      String message = String(xPositions[i]) + String(yPositions[i]) + String(vel);
      Serial.println(message);
      delay(10);
    }  
  }
}
