#pragma once

/* =========================================================
   Helper class: TurnTracker (NO reset logic inside)
   ========================================================= */


#define CS_PIN 61
bool spi = true;

// Add these constants at the top (after the gyro declaration)
const float TARGET_ANGLE_TOLERANCE = 3.0;  // Degrees tolerance
const float GYRO_KP = 0.8;  // Proportional gain for gyro
const int GYRO_MIN_PWM = 27;
const int GYRO_MAX_PWM = 45;


// Speed tracking variables - add these globally
volatile unsigned long m1_last_pulse_time = 0;
volatile unsigned long m2_last_pulse_time = 0;
volatile unsigned long m1_pulse_interval = 0;  // Microseconds between pulses
volatile unsigned long m2_pulse_interval = 0;

unsigned long lastPrintTime1 = 0;
unsigned long lastPPS = 0;

unsigned long lastResetTime = 0;

const unsigned long PRINT_INTERVAL = 500;   // 0.5 second
const unsigned long RESET_INTERVAL = 5000;  // 5 seconds


const int BRAKE_PWM = 270;              // PWM for reverse braking
const int BRAKE_DURATION_MS = 8;      // How long to apply brake
const int COAST_AFTER_BRAKE_MS = 100;   // Let it settle after braking
// Speed control parameters
const int MIN_PWM = 290;           // Minimum PWM to keep motor moving

const int MIN_PWM_TURN_M1 = 245;           // Minimum PWM to keep motor moving
const int MIN_PWM_TURN_M2 = 245-40;           // Minimum PWM to keep motor moving



const int MIN_PWM_M2 = 200;           // Minimum PWM to keep motor moving

const int MAX_PWM = 320;           // Minimum PWM to keep motor moving
const int MAX_PWM_M2 = MAX_PWM+150;           // Minimum PWM to keep motor moving

const int MAX_PWM_TURN = 320;           // Minimum PWM to keep motor moving
const int MAX_PWM_TURN_M2 = MAX_PWM+150;           // Minimum PWM to keep motor moving

const int MAX_PWM_STRAIGHT = 320;           // Minimum PWM to keep motor moving
const int MAX_PWM_STRAIGHT_M2 = MAX_PWM+150;           // Minimum PWM to keep motor moving
const int DECEL_START_PULSES = 35; // Start slowing down this many pulses before target

// Dynamic inertia stop configuration
const float STOP_START_PERCENT = 50.0;  // Start stops after 50% completion
const int MAX_STOP_DELAY = 300;         // Maximum stop delay in ms
const int MIN_STOP_DELAY = 25;          // Minimum stop delay in ms
const int STOP_INTERVAL_LOOPS = 1;      // Apply stop every N loops when in stop zone

// PID state variables for M2
float m2_integral = 0;
float m2_previous_error = 0;

long m1_last = 0;
long m2_last = 0;
unsigned long lastTime = 0;

int gm1_pwm = 350;
int gm2_pwm = 330;  // M2 is faster, so slightly lower PWM



// Motor specifications - Based on measurements: 2600 steps = 5 ft (1524 mm)
const int PULSES_PER_REV = 720;  // Measured: encoder steps per wheel rotation
//const float WHEEL_DIAMETER_MM = 50.8 *1.25 ; //0.5 inch bigger  // 2 inches diameter
//const float WHEEL_DIAMETER_MM =20;// 70 /factor ; //0.5 inch bigger  // 2 inches diameter


const float WHEEL_CIRCUMFERENCE_MM = WHEEL_DIAMETER_MM * PI;  // = 159.59 mm
const float PULSES_PER_MM1 = PULSES_PER_REV / WHEEL_CIRCUMFERENCE_MM;  // = 1.706 steps/mm


// Robot specifications
const float WHEEL_BASE_MM1 = 50;//130.0 / factor;  // Distance between wheel centers - CALIBRATE THIS!
const float TURN_CIRCUMFERENCE_MM = WHEEL_BASE_MM1 * PI;
const long PULSES_FOR_90_TURN1 = (TURN_CIRCUMFERENCE_MM / 4.0) * PULSES_PER_MM1 * 2;  // Quarter circle

const long PULSES_FOR_90_TURN=480;//#466




int commandIndex = 0;

// Debug control - DISABLED BY DEFAULT
bool debugEnabled = false;
const unsigned long SERIAL_TIMEOUT = 100;  // ms to wait for Serial









inline int getStopDelayGyro(float error_degrees) {
  float abs_error = abs(error_degrees);
  
  // No delay if far from target
  if (abs_error > 45.0) {
    return 0;
  }
  
  // Calculate how close we are (0.0 = far, 1.0 = at target)
  float proximity = 1.0 - (abs_error / 45.0);  // 0-45° mapped to 0.0-1.0
  
  // Exponential curve for more aggressive stopping near target
  float curve_factor = proximity * proximity * proximity;  // Cubic for aggressive curve
  
  // Calculate delay
  int delay_ms = MIN_STOP_DELAY + (int)((MAX_STOP_DELAY - MIN_STOP_DELAY) * curve_factor);
  
  // Scale based on how close we are
  if (abs_error < 5.0) {
    delay_ms *= 3;  // Triple delay when very close
  } else if (abs_error < 15.0) {
    delay_ms *= 2;  // float delay when close
  }
  
  return constrain(delay_ms, 0, MAX_STOP_DELAY * 3);
}


float getCompletionPercentGyro(float turned_degrees, float target_degrees) {
  float abs_turned = abs(turned_degrees);
  float abs_target = abs(target_degrees);
  
  if (abs_target == 0) return 100.0;
  
  float percent = (abs_turned / abs_target) * 100.0;
  return constrain(percent, 0.0, 100.0);
}

int getM1SpeedGyro(float remaining_degrees, int base_pwm) {
  float abs_remaining = abs(remaining_degrees);
  
  // Linear deceleration zone (when remaining < 40°)
  if (abs_remaining < 40.0) {
    // Linear deceleration from base_pwm down to MIN_PWM_TURN_M1 (100)
    int speed_range = base_pwm - 150;
    int scaled_pwm = 150 + (int)((speed_range * abs_remaining) / 40.0);
    return constrain(scaled_pwm, 100, base_pwm);
  }
  
  // Full speed when far from target
  return base_pwm;
}


float KP =4.0;
float KI =0.1;
float KD =0.1;



int getM2SpeedGyro(int p_m1_pwm, long m1_count, long m2_count, int current_m2_pwm) {
  // Calculate position error (positive = M2 is behind M1)
  long position_error = m1_count - m2_count;
  
  // PID calculations
  m2_integral += position_error;
  m2_integral = constrain(m2_integral, -500, 500);  // Anti-windup
  
  float derivative = position_error - m2_previous_error;
  m2_previous_error = position_error;
  
  // PID output
  float pid_adjustment = (KP * position_error) + 
                         (KI * m2_integral) + 
                         (KD * derivative);
  
  // Apply adjustment to M2 PWM
  int adjusted_pwm = current_m2_pwm + (int)pid_adjustment;
  
  // Constrain - M2 can go slightly faster than M1 to catch up
  adjusted_pwm = constrain(adjusted_pwm, current_m2_pwm-50, current_m2_pwm+50);
  
  return adjusted_pwm;
}
