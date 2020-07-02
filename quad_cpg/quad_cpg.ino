#include "Arduino.h"
#include <Servo.h>
#include <math.h>

#define SERVO0_PIN 2
#define SERVO1_PIN 3
#define SERVO2_PIN 4
#define SERVO3_PIN 5
#define SERVO4_PIN 6
#define SERVO5_PIN 7
#define SERVO6_PIN 8
#define SERVO7_PIN 9
#define LPERIOD 10000L  // loop period time in us.
#define N 4 // number of oscillators
#define T LPERIOD/1000000.0 // T=10ms.

unsigned long nextLoop;
float a, b, c, d;, Tu, Tv, Su, Sv, mu, p, alpha_k, alpha_h, A_h, A_k;
float W[N][N];

int i,j;

float su[N]={0,0,0,0}; // phase
float sv[N]={0,0,0,0};
float sy_k[N]={0,0,0,0};
float sy_h[N]={0,0,0,0};
float sr[N]={0,0,0,0}; // amplitude
float sx[N]={0,0,0,0}; // offset
float sv_new[N]={0,0,0,0};
float su_new[N]={0,0,0,0}; // phase
float sr_new[N]={0,0,0,0}; // amplitude
float sx_new[N]={0,0,0,0}; // offset

// derivatives
float su_d[N]={0,0,0,0};
float sv_d[N]={0,0,0,0};// phase dot
float sy_h_d[N]={0,0,0,0}
float sr_d[N]={0,0,0,0}; // amplitude dot
float sx_d[N]={0,0,0,0}; // offset dot
float sr_d_new[N]={0,0,0,0}; // amplitude dot
float sx_d_new[N]={0,0,0,0}; // amplitude dot

float out[2*N]={0,0,0,0,0,0,0,0};
float temp;

Servo servo0;
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;
Servo servo6;
Servo servo7;

void setup() {
  // put your setup code here, to run once:
  servo0.attach(SERVO0_PIN);
  servo1.attach(SERVO1_PIN);
  servo2.attach(SERVO2_PIN);
  servo3.attach(SERVO3_PIN);
  servo4.attach(SERVO4_PIN);
  servo5.attach(SERVO5_PIN);
  servo6.attach(SERVO6_PIN);
  servo7.attach(SERVO7_PIN);
  
  W[1][1] = 0;
  W[1][2] = -0.1;
  W[1][3] = -0.1;
  W[1][4] = -0.1;
  W[2][1] = -0.1;
  W[2][2] = 0;
  W[2][3] = -0.1;
  W[2][4] = -0.1;
  W[3][1] = -0.1;
  W[3][2] = -0.1;
  W[3][3] = 0;
  W[3][4] = -0.1;
  W[4][1] = -0.1;
  W[4][2] = -0.1;
  W[4][3] = -0.1;
  W[4][4] = 0;

  nextLoop = micros() + LPERIOD;
}

void get_du(){
  temp=0.0;
  for(i=0; i<N; i++){
    for(j=0; j<N; j++){
       temp=W[i][j]*su[j];
      }
    su_d[i]=(tanh(mu*(a*su[i]-b*sv[i]+temp+Su))-su[i])/Tu;
    }
}

void get_dv(){
  temp=0.0;
  for(i=0; i<N; i++){
    for(j=0; j<N; j++){
       temp=W[i][j]*sv[j];
      }
    su_d[i]=(tanh(mu*(c*su[i]-d*sv[i]+temp+Su))-sv[i])/Tv;
    }
}

void loop() {
  // put your main code here, to run repeatedly:
  for(i)
}
