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
float a, b, c, d, Tu, Tv, Su, Sv, mu, p, alpha_k, alpha_h, A_h, A_k;
float W[N][N];
float R_h, R_k, X;

int i,j;

float su[N]={0,0,0,0}; // phase
float sv[N]={0,0,0,0};
float sy_k[N]={0,0,0,0};
float sy_h[N]={0,0,0,0};
float sv_new[N]={0,0,0,0};
float su_new[N]={0,0,0,0}; // phase

// derivatives
float su_d[N]={0,0,0,0};
float sv_d[N]={0,0,0,0};// phase dot
float sy_h_d[N]={0,0,0,0};

float out[2*N]={0,0,0,0,0,0,0,0};
float temp_u, temp_v;

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
  Serial.begin(9600);
  servo0.attach(SERVO0_PIN);
  servo1.attach(SERVO1_PIN);
  servo2.attach(SERVO2_PIN);
  servo3.attach(SERVO3_PIN);
  servo4.attach(SERVO4_PIN);
  servo5.attach(SERVO5_PIN);
  servo6.attach(SERVO6_PIN);
  servo7.attach(SERVO7_PIN);
  
  W[1][1] = 0.0;
  W[1][2] = -0.1;
  W[1][3] = -0.1;
  W[1][4] = -0.1;
  W[2][1] = -0.1;
  W[2][2] = 0.0;
  W[2][3] = -0.1;
  W[2][4] = -0.1;
  W[3][1] = -0.1;
  W[3][2] = -0.1;
  W[3][3] = 0.0;
  W[3][4] = -0.1;
  W[4][1] = -0.1;
  W[4][2] = -0.1;
  W[4][3] = -0.1;
  W[4][4] = 0.0;

  Tu=0.2;
  Tv=0.2;
  a=5.6;
  b=5.6;
  c=2.4;
  d=-2.4;
  Su=0.02;
  Sv=0.02;
  p=0.5;
  mu=1.0;
  A_h=1.0;
  A_k=0.91;
  alpha_k=1.0;
  alpha_h=0.75;
  R_h=35.55;
  R_k=21.12;
  X=0.0;
  
  nextLoop=micros()+LPERIOD;
}

void set_du_dv(){
  for(i=0;i<N;i++){
    temp_u=0.0;
    temp_v=0.0;
    for(j=0; j<N; j++){
       temp_u += W[i][j]*su[j];
       temp_v += W[i][j]*sv[j];
      }
    su_d[i]=(tanh(mu*(a*su[i]-b*sv[i]+temp_u+Su))-su[i])/Tu;
    sv_d[i]=(tanh(mu*(c*su[i]-d*sv[i]+temp_v+Sv))-sv[i])/Tv;
    }
  }

void loop() {
  // put your main code here, to run repeatedly:
  set_du_dv();
  for(i=0;i<N;i++){
    su[i] += su_d[i]*T;
    sv[i] += sv_d[i]*T;
    sy_h[i]=p*(su[i]-sv[i]);
    sy_h_d[i]=p*(su_d[i]-sv_d[i]);
    if(sy_h_d[i]<0){
      sy_k[i]=0;
      }
    else{
      sy_k[i]=alpha_k*A_k*(1-(sy_h[i]/(alpha_h*A_h))*(sy_h[i]/(alpha_h*A_h)));
      }
    out[i]=X+R_h*sin(sy_h[i]);
    out[i+4]=R_k*sin(sy_k[i]);
    }
  servo0.write( 90 + round(out[0]) );
  servo1.write( 90 + round(out[1]) );
  servo2.write( 90 + round(out[2]) );
  servo3.write( 90 + round(out[3]) ); 
  servo4.write( 90 + round(out[4]) );
  servo5.write( 90 + round(out[5]) );
  servo6.write( 90 + round(out[6]) );
  servo7.write( 90 + round(out[7]) );
  /**
  Serial.print(sy_h[0]);
  Serial.print("\t");
  Serial.print(sy_h[1]);
  Serial.print("\t");
  Serial.print(sy_h[2]);
  Serial.print("\t");
  Serial.println(sy_h[3]);

  Serial.print(sy_k[0]);
  Serial.print("\t");
  Serial.print(sy_k[1]);
  Serial.print("\t");
  Serial.print(sy_k[2]);
  Serial.print("\t");
  Serial.println(sy_k[3]); **/
  
  while(nextLoop > micros());  //wait until the end of the time interval
  nextLoop += LPERIOD;  
}
