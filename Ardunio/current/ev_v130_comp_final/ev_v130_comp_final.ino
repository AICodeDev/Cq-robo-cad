#include "conf.h"

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
//#include "control_robo.h"
//#include "RB_GYRO_FAST.h"

#include "tracking_corr.h"

#include "command.h"
#include "RB_BUZZER.h"
#include "RB_RGBLED.h"
#define RGB_LED_PIN 44
//#define USER_KEY_Pin 35
#define BUZZER_Pin 36  // Change to your buzzer pin
#define LIGHT_PIN 13
RB_RGBLed RGBLED(RGB_LED_PIN, 2);

RB_Buzzer buzzer(BUZZER_Pin);

RB_Serial RB_Serial;

uint8_t Device_ID;




RB_EncoderMotor M1(1);
RB_EncoderMotor M2(2);

extern DistanceSelector selector;

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

    
    delay(5);

 //   Serial.println("stat");
    
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

    pinMode(USER_KEY_Pin, INPUT_PULLUP);
    pinMode(Buzzer_Pin, OUTPUT);

   setupSpeedTimer();

#if DEBUG
    Serial.println("Mial");
    Serial.println(millis());
    
#endif
    curr={0};
      delay(1000);
//LED

  pinMode(LIGHT_PIN, OUTPUT);
  // Initialize RGB LED
  RGBLED.setColor(1, 50, 0, 0); // Red during initialization
  RGBLED.show();

   mainProgram();


   //StartNextTourCommand();
}






void resetCommands(){

}
void onPressB() {
    Serial.println("Button Pressed55");
    resetCommands();
    delay(2000);
    TestMove();
}

void checkButtonPress() {
    bool current_reading = (digitalRead(USER_KEY_Pin) == LOW);
    unsigned long now = millis();

    // 1. Only act if the state has changed (from not pressed to pressed)
    // 2. Only act if enough time has passed (debounce)
    if (current_reading && !button_was_pressed && (now - last_debounce_time > debounce_delay)) {
        onPressB();
        last_debounce_time = now; // Update the timer
    }

    button_was_pressed = current_reading;
}


void loop(){    
  checkButtonPress();
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
 //// m2_integral = 0;
 // m2_previous_error = 0;
}
//long m1_pending =0;
//l//ong m2_pending =0;





void TestMove(){
      curr={0};
    
    float pulse_per_mm = 1.98;
    
   
 #if DEBUG
        //printDebugStatus();
     //   LOG_INFO3(" PWM 1/2", pwm1, pwm2);
       DEBUG_PRINT("xxx");
       DEBUG_PRINT(".");
       
      PrintMove();
       

#endif

    moveEvPulse( 17000 ,1);

    delay(500);
    Serial.println("d");
 

}



void mainProgram(){
 // Serial.println("Main");
   checkButtonCount();
  //TestMove();
}


void mainRun(long targetInCm){
  Serial.println("Main Run - Pulse per cm");
  Serial.println(PULSE_PER_CM);
  
  long pulse = targetInCm * PULSE_PER_CM;
  Serial.println("Main Run - pulse ");
  Serial.println(pulse);
  moveEvPulse( 17000 ,1);

  delay(500);
  Serial.println("complete");


}


void checkButtonCount() {
  int baseDistance = 675 ; //cm inc 25 cm
  while (1)
  {

    Button_Process();
  
  // After 2 seconds of no press, enter wait_for_start mode
    if (!wait_for_start && button_count > 0) {
      if (millis() - last_press_time >= 5000) {
        wait_for_start = true;
        target_distance = button_count * 25 + baseDistance ;
        
        // Beep 500ms when entering wait_for_start
        buzzer.tone(800, 1500);
        
        Serial.print("Distance set: ");
        Serial.print(target_distance);
        Serial.println("m. Press button to START");
      }
    }
  
  // In wait_for_start mode, if button pressed, wait 1 sec then start
    if (wait_for_start && start_press_time > 0) {
      if (millis() - start_press_time >= 1000) {
        
        // Beep 1 second when motor starts
        buzzer.tone(500, 500);
        mainRun(target_distance);
        
       // Serial.println("MOTOR STARTED!");
        
        // Reset
        button_count = 0;
        wait_for_start = false;
        start_press_time = 0;
      }
    }
  }

}

void Button_Process() {
  if (digitalRead(USER_KEY_Pin) == HIGH) {
    Hardware_Button_flag = true;
  }
  
  if (digitalRead(USER_KEY_Pin) == LOW && Hardware_Button_flag) {
    Button_Down = true;
    Hardware_Button_flag = false;
  }
  
  if (Button_Down) {
    Button_Down = false;
    
    if (!wait_for_start) {
      // Count distance
      button_count++;
        RGBLED.setColor(1, 25, 25, 25); // White flash
        RGBLED.show();
        delay(50);
        RGBLED.setColor(1, 0, 50, 0); // Green
        RGBLED.show();

      last_press_time = millis();
      
      // Beep 50ms if count is divisible by 5
    //  if (button_count % 2 == 0) 
    {
       //  Serial.print("button_count % 5 == 0");
        //Serial.println("small beep");
        buzzer.tone(1500, 100);

      }
      
      Serial.print("c: ");
      Serial.print(button_count);
      Serial.print(" = ");
      Serial.print(button_count * 25 + 675);
      Serial.println(" cm");
    } else {
      // Start button pressed
      start_press_time = millis();
     // Serial.println("Starting in 1 second...");
    }
  }
}
