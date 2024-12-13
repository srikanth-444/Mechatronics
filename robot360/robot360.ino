#include <SparkFun_TB6612.h>

// motor driver 1 (front wheels)
#define FAIN1 50 // right ground
#define FAIN2 52 // right drive
#define FPWMA 10 

#define FBIN1 51 // left ground
#define FBIN2 53 // left drive
#define FPWMB 8

#define FSTBY 9

// motor driver 2 (rear wheels)
#define RAIN1 38
#define RAIN2 40
#define RPWMA 13

#define RBIN1 39
#define RBIN2 41
#define RPWMB 11

#define RSTBY 12

const int offset = 1;

int r=0.04;
int lx=0.0725;
int ly=0.105;

// initializing motors (in order: FR, FL, RR, RL)
Motor motor1R = Motor(FAIN1, FAIN2, FPWMA, offset, FSTBY);
Motor motor1L = Motor(FBIN1, FBIN2, FPWMB, offset, FSTBY);
Motor motor2R = Motor(RAIN1, RAIN2, RPWMA, offset, RSTBY);
Motor motor2L = Motor(RBIN1, RBIN2, RPWMB, offset, RSTBY);

#define   ARR_SIZE   6
byte values[ARR_SIZE];    // float/doubles are the same on AVR8

// returns true when a new array of values has been
// received and is ready for further processing.
// Otherwise returns false.
void setup() {
    Serial.begin(115200);  
}

void loop() {
  Serial.write("started");
    if (Serial.available() > 0) {
      Serial.readBytes(values,6);   
    }
    int vx = (int)values[0]*(int)values[1];
    int vy = (int)values[2]*(int)values[3];
    int wz = (int)values[4]*(int)values[5];
    drive(vx, vy, wz);
    // do other stuff..
}

void drive(int vx, int vy, int wz) {
  int wfr=(vx + vy + (lx+ly)*wz )/r
  int wfl=(vx - vy - (lx+ly)*wz )/r
  int wrr=(vx - vy + (lx+ly)*wz )/r
  int wrl=(vx + vy - (lx+ly)*wz )/r
  motor1R.drive(wfr);
  motor1L.drive(wfl);
  motor2R.drive(wrr);
  motor2L.drive(wrl);
}

