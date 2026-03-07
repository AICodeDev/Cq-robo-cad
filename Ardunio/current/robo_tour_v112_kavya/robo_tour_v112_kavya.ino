#include "RB_ENCONDERMOTOR.h"
#include "cons.h"
#include "vars.h"
//#include "pid.h"
#include "utils.h"
#include "motor_helper.h"
#include "gyro_icm_var.h"
#include "gyro_pure_function.h"
#include "move.h"
#include "turn.h"

#include "RB_PORT.h" 
#include "RB_SERIAL_TASK.h" 
#include "RB_QMIND_PLUS.h"
#include "RB_GYRO.h"
#include "control_robo.h"
//#include "RB_GYRO_FAST.h"

#include "tracking_corr.h"

#include "command.h"


RB_Serial RB_Serial;
RB_GYRO   gyro(2);
//* Top LEFT BLUE MISO
//* MIddle LEFT YELLOE SCK
//* MIddle RIGHT GRREN MOSI
#if USE_RB_GYRO_FAST
//  RB_GYRO_FAST   gyro(2);
#endif


uint8_t Device_ID;




RB_EncoderMotor M1(1);
RB_EncoderMotor M2(2);

#if USE_RB_GYRO == 0
#include <SPI.h>
#include <ICM20948_WE.h>
ICM20948_WE myIMU(&SPI, CS_PIN, spi);

#endif

// ---------- Encoder ISRs ----------
void ISR_M1() { curr.total_pulse.m1++; curr.current_pulse.m1++;  }
void ISR_M2() { curr.total_pulse.m2++; curr.current_pulse.m2++; }

inline void UpdateRobotOdometry()
{
    // --- Read encoder deltas ---
    long m1_now = (curr.total_pulse.m1);
    long m2_now = (curr.total_pulse.m2);

    long dP1 = m1_now - m1_pulses_odo_last;
    long dP2 = m2_now - m2_pulses_odo_last;

    m1_pulses_odo_last = m1_now;
    m2_pulses_odo_last = m2_now;

    // --- Save previous heading ---
    robotPose.prevHeading = robotPose.heading;

    // --- Differential drive kinematics (pulse space) ---
    float dCenter = (dP1 + dP2) * 0.5f;   // pulses
    float dTheta  = (float)(dP2 - dP1) / WHEEL_BASE_PULSES; // radians

    // --- Midpoint integration (important for curves) ---
    float headingMid = robotPose.heading + dTheta * 0.5f;

    robotPose.x += (long)(sin(headingMid) * dCenter);
    robotPose.y += (long)(cos(headingMid) * dCenter);

    robotPose.heading += dTheta;

    // --- Normalize heading (-PI .. PI) ---
    if (robotPose.heading > PI)  robotPose.heading -= 2.0f * PI;
    if (robotPose.heading < -PI) robotPose.heading += 2.0f * PI;
}


// ---------- PWM control ----------





void setup() {
    Serial.begin(115200);
    Serial3.begin(115200);
    RB_Serial.Serial_begin(115200);

    
    delay(500);

   
    pinMode(M1_ENA_A,INPUT_PULLUP);
    pinMode(M1_ENA_B,INPUT_PULLUP);

    pinMode(M2_ENA_A,INPUT_PULLUP);
    pinMode(M2_ENA_B,INPUT_PULLUP);


    pinMode(M1_MOTOR_PWMA, OUTPUT);
    pinMode(M1_MOTOR_PWMB, OUTPUT);
    
    pinMode(M2_MOTOR_PWMA, OUTPUT);
    pinMode(M2_MOTOR_PWMB, OUTPUT);

   //enable PWN Timers
   pinMode(20, OUTPUT);
   digitalWrite(20, HIGH);

   attachInterrupt(M1_INT, ISR_M1, CHANGE);
   attachInterrupt(M2_INT, ISR_M2, CHANGE);
  

   setMotor1(0); //will set the   OCR1A = 0;  OCR1B = 0;
   setMotor2(0);
#if USE_ICM_GYRO 
    DEBUG_PRINTLN("ICM SETUP");
    setupGyro();
#endif

#if USE_RB_GYRO_FAST 
      //setupRBGyro();
      gyro.start();
      delay(50);
      gyro.updateZ();
#endif

  //Button
//const int BUTTON_PIN = USER_KEY_Pin;
//const int BUZZER_PIN = BUZZER_Pin;  // Change to your buzzer pin
//#define Buzzer_Pin     36
    pinMode(USER_KEY_Pin, INPUT_PULLUP);
    pinMode(Buzzer_Pin, OUTPUT);

   setupSpeedTimer();

   mainProgram();


   //StartNextTourCommand();
}


void setupRBGyro(){

#if USE_RB_GYRO
  gyro.begin();
  delay(50);
  gyro.ReadData(0x75,&Device_ID,1);
  DEBUG_PRINTLN("setupRBGyro Who am I:");
  DEBUG_PRINTLN(Device_ID);
#endif 

}


float updateRBGyroFast(){

#if USE_RB_GYRO_FAST 
    //Serial.println("updateRBGyro");

    float localZ= gyro.updateZ();
    gyroRBUpdate(localZ);
    
    return (localZ);

   // return localZ;

#endif 
  return 0;

}


float updateRBGyro(){

#if USE_RB_GYRO_FAST 
    return updateRBGyroFast();
#endif 

#if USE_RB_GYRO 
    //Serial.println("updateRBGyro");

    gyro.Update();
    float z = (gyro.getAngleZ());
  //  DEBUG_PRINTLN(z);
    z= normalizeRBAngle(z);
  //  DEBUG_PRINTLN(z);
    //Serial.println(z);
    gyroRBUpdate(z);
    return abs(turnTracker.getLocal());

    return z;

#endif 


}

void resetCommands(){

}
void onPress() {
    Serial.println("Button Pressed");
    resetCommands();
    delay(2000);
    excuteCommmandAll();
    // Trigger buzzer or other logic here
}

void checkButtonPress() {
    bool current_reading = (digitalRead(USER_KEY_Pin) == LOW);
    unsigned long now = millis();

    // 1. Only act if the state has changed (from not pressed to pressed)
    // 2. Only act if enough time has passed (debounce)
    if (current_reading && !button_was_pressed && (now - last_debounce_time > debounce_delay)) {
        onPress();
        last_debounce_time = now; // Update the timer
    }

    button_was_pressed = current_reading;
}


void loop(){    
  checkButtonPress();
}



// Debug print macros - only print if debug enabled AND Serial connected
float updateGyro()
{

#if USE_RB_GYRO_FAST
  return updateRBGyroFast();
#endif 

#if USE_RB_GYRO
  return updateRBGyro();
#endif 

#if USE_ICM_GYRO 
  myIMU.readSensor();
  xyzFloat gyr;
  myIMU.getGyrValues(&gyr);   // deg/s
  turnTracker.update(gyr.z);
  return abs(turnTracker.getLocal());

#endif

  return abs(turnTracker.getLocal());

}


void setupGyro() {
 
 #if USE_ICM_GYRO
   BLE_LOG("setupGyro");
  int found =0;
  while(found<3)
  {
    

    while (!myIMU.init()) {
      Serial.println("*No ICM*\n");

      BLE_LOG("**No ICM \n");
      found--;
      delay(800);
      }
      found++;
      BLE_LOG("ICM FIND\n  detected!!!!!!!");
      delay(100);
     //  DEBUG_PRINTLN("Findaa");
  }

  BLE_LOG("gyro (keep still)");
  delay(100);
  myIMU.autoOffsets();
  delay(100);
  myIMU.autoOffsets();
  delay(100);
  myIMU.autoOffsets();
  delay(100);
  myIMU.autoOffsets();



  myIMU.setGyrRange(ICM20948_GYRO_RANGE_250);
  myIMU.setGyrDLPF(ICM20948_DLPF_6);
    BLE_LOG("Calibrating gyro (keep still)=done");
#endif

#if USE_RB_GYRO
  DEBUG_PRINTLN("Start - setupGyro RB USE_RB_GYRO");
  gyro.begin();
  delay(50);
  gyro.ReadData(0x75,&Device_ID,1);
  Serial.print("XX Who am I:");
  Serial.println(Device_ID);

#endif


  turnTracker.begin();

  lastPrintTime = millis();
  lastResetTime = millis();
}


int getStopDelay(float completion_percent) {
  // Don't stop if we haven't reached the threshold
  if (completion_percent < STOP_START_PERCENT) {
    return 0;
  }
  
  // Calculate how far into the stop zone we are (0.0 to 1.0)
  float stop_zone_progress = (completion_percent - STOP_START_PERCENT) / (100.0 - STOP_START_PERCENT);
  
  // Apply exponential curve for more aggressive stopping near target
  // Using quadratic curve: delay increases faster as we get closer
  float curve_factor = stop_zone_progress * stop_zone_progress;
  
  // Calculate delay with exponential increase
  int delay_ms = MIN_STOP_DELAY + (int)((MAX_STOP_DELAY - MIN_STOP_DELAY) * curve_factor);
  
  return constrain(delay_ms, MIN_STOP_DELAY, MAX_STOP_DELAY)*1;
}



//int m1_current_pwm = 0;
//int m2_current_pwm = 0;


void resetPID() {
  m2_integral = 0;
  m2_previous_error = 0;
}
//long m1_pending =0;
//l//ong m2_pending =0;





void TestMove(){
    movePulse(1091,1);
    delay(500);
 

}



void TestTurn(){
      DEBUG_PRINTLN(i);
    //(1091 * 50) /62
   // movePulse(1091*2,1);
    applyBreak();

       applyBreak();
    DEBUG_PRINTLN("*");
    DEBUG_PRINTLN("*");
    delay(1500);
 

}










 void R(){
   
 } 

 void MDirectio(){
    movePulse(380*1.95);
    StopMotors();
    delay(1000);
 }
void TestGryo(){
  
  float z= updateGyro();
  DEBUG_PRINT("AAA z:");
  
  DEBUG_PRINTLN(z);

  delay(50);

}

void mainProgram(){
  excuteCommmandAll();
}

 void mainProgram2(){
  curr = CURR_INT;
  delay(1000);
 // Serial.println("Start");
  #if  USE_RB_GYRO 
    gyro.begin();
    gyroBegin();
  #endif


  DEBUG_PRINTLN("Mg");

  //  Serial.print("Recommended: M1_SPEED_MULTIPLIER = ");
  //  setupGyro();
    curr.lastMicros = micros();
   // TestMove();
    
    for (int i=0;i<5;i++)
    {
      TestMove();

    #if  USE_RB_GYRO 
      gyro.begin();
      gyroBegin();
    #endif

      TestTurn();
    
      StopMotors();
      delay(200);
  

    
  }
    StopMotors();

    applyBreak();
   // StopMotors();
    while(1){

       DEBUG_PRINT("^");
   
       delay(2000);

    }

 }


