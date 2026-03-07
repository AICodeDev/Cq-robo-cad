#pragma once

#include "SafeLogger.h"
#include "debug_macro.h"

extern SafeBleLogger bleLogger;

;
#define PrintPort Serial
#define PrintSep ","

#define USE_ICM_GYRO 1
#define USE_RB_GYRO 0
#define USE_RB_GYRO_FAST 0

#define USE_RB_GYRO_VERSION 0


//..#define GYRO RB_GYRO_FAST

#define BLUE_WHEEL 1 
#define TURN_PULSE_MAX 750 

#define TOLERANCE_PULSE_MOVE  80
#define TOLERANCE_PULSE_TURN  80

#define EXTRA_FULL_PULSE  30
#define EXTRA_HALF_PULSE  10

#define BLUE_DIA   55
#define FULL_PULSE_OLD  1250
#define FULL_PULSE_BLUE  1389

#define FULL_PULSE  (1389) //50 Cm 

#define PULSE_PER_CM  (1389/50)


#define SLOW_DOWN_PULSE  (FULL_PULSE/2)


//(1091 *0.6)
#define MY_90 72
#define MY_90_PULSE (480)
#define MY_90_PULSE_MAX (540) //#todo adjust 


#define HALF_PULSE  ((FULL_PULSE/2)-25) 

/************ DEBUG MACROS ************/

#define REMOTE_DEBUG   DEBUG  // set to 0 to disable all debug logs for BL DEBUG 
#define TURN_TOLERENCE (0.5f) 


#if DEBUG
  #define DEBUG_PRINT(x)          Serial.print(x);
  #define DEBUG_PRINTLN(x)        Serial.println(x);
  #define DEBUG_PRINTX3(a1,b1,c1)     Serial.print(a1); Serial.print(PrintSep); Serial.print(b1); Serial.print(PrintSep); Serial.print(c1) ;
  #define DEBUG_PRINT4(a,b,c,d)   
  #define DEBUG_PRINT5(a,b,c,d,e) 
  

  
  
  #define DEBUG_PRINT2(a,b)   Serial.print(a); Serial.print(" : "); Serial.print(b); Serial.print("  "); 
  


  // printf-style debug (Arduino-safe)
  #define DEBUG_PRINTF(fmt, ...)              \
    do {                                      \
      char __dbg_buf[128];                    \
      snprintf(__dbg_buf, sizeof(__dbg_buf), fmt, ##__VA_ARGS__); \
      Serial.print(__dbg_buf);                \
    } while (0)
#else
  #define DEBUG_PRINT(x)
  #define DEBUG_PRINTLN(x)
  #define DEBUG_PRINTF(fmt, ...)
  #define DEBUG_PRINTX3(a,b,c)
  #define DEBUG_PRINT2(a,b)
  #define DEBUG_PRINT4(a,b,c,d)   
  #define DEBUG_PRINT5(a,b,c,d,e) 

#endif
/****************************************/



#define M1_ENA_A          19
#define M1_ENA_B           9

#define M2_ENA_A          18
#define M2_ENA_B           8

#define EN_A_A          19
#define EN_A_B           9
#define EN_B_A          18 
#define EN_B_B           8


#define M1_INT           4
#define M2_INT           5

#define LowPowr_Pin    66

#define M_MOTOR_PWM0     11
#define M_MOTOR_PWM1     12
#define M_MOTOR_PWM2     6
#define M_MOTOR_PWM3     7
#define M_MOTOR_Charge_Pin    20
#define M_MOTOR_Sleep_Pin     17
#define M_MOTOR_Fault_Pin     16


#define M1_MOTOR_PWMA     11
#define M1_MOTOR_PWMB     12


#define M2_MOTOR_PWMA     6 
#define M2_MOTOR_PWMB     7

#define SAMPLE_MS      100    // speed sample period
#define SAMPLE_MS_PPS    50    // speed sample period

#define PWM_MAX     1000

#define MM_PER_PULSE      0.5f      // given by you
//#define WHEEL_BASE_MM     120.0f    // <<< MEASURE THIS
#define DEG_PER_RAD       57.2957795f


#define STEP_MM             0.5f
//#define WHEEL_BASE_MM       160.0f
#define CONTROL_DT_MS       100


#define FORWARD_DIST_MM     250.0f     // 25 cm
#define TURN_RADIUS_MM      250.0f
#define TURN_ANGLE_RAD      (PI / 2)

#define ARC_STEPS           20
#define SOFT_BRAKE_PPS      30

#define PULSES_PER_MM   (3000.0f / 1200.0f)   // = 2.5 pulses per mm
#define MM_PER_PULSE   (1.0f / PULSES_PER_MM)

#define WHEEL_BASE_PULSES 200
#define WHEEL_BASE_PULSE 200


#define FORWARD_DIST_MM   250.0f   // 25 cm
#define FORWARD_PULSES    (FORWARD_DIST_MM * PULSES_PER_MM)
#define MOVE_COMPLETE_PULSE  50


//###define PULSES_PER_CM (3000.0f / 120.0f) 

#define FORWARD_DIST_MM 250
#define FORWARD_PULSES  (FORWARD_DIST_MM * PULSES_PER_MM)


#include <Arduino.h>

/* =========================================================
   ================== CONFIG CONSTANTS =====================
   ========================================================= */

////#define WHEEL_BASE_MM        160.0f     // distance between wheels
//#define WHEEL_BASE_PULSE        160.0f     // distance between wheels

#define STEP_MM              0.5f       // 1 pulse = 0.5mm

#define MIN_PPS              20
#define MAX_PPS              300

#define PWM_MIN              50
#define PWM_MAX              320

#define SOFT_BRAKE_PPS       30

#define CONTROL_DT_MS        20          // control loop period

#define FORWARD_CM            25.0
#define ARC_SEGMENTS          20
#define DEFAULT_CRUISE_PPS    350
#define MIN_PPS               80
#define MAX_PPS               450
#define PWM_STEP_LIMIT 5   // max change per PID update


// ===== ROBOT CONSTANTS =====

// Wheel parameters
const float WHEEL_DIAMETER_MM = 70.0;
const float WHEEL_DIAMETER_CM = 7.0;
const float WHEEL_CIRCUMFERENCE_CM = 21.991;   // π × 7 cm

// Encoder
const int ENCODER_PPR = 480;

// Movement conversion
const float PULSES_PER_CM = 21.83;

// Robot geometry
const float WHEEL_BASE_MM = 120.0;
const float WHEEL_BASE_CM = 12.0;

// Turning
const float PULSES_PER_90_DEG = 206.0;

#define PPS_HALT_THRESH        15     // pulses/sec → essentially stopped
#define HALT_COUNT_TRIGGER     4      // consecutive detections
#define BOOST_STEP             3
#define BOOST_MAX              40
#define BOOST_DECAY            1
#define MIN_REMAINING_PULSE    120

#define m1_count m1_pulsescc
#define m2_count m2_pulsescc