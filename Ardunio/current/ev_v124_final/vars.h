#pragma once

#include "types.h"
#include "ev_type.h"
#include "ev_var.h"
#include "RB_Port.h"

const float STOP_START_PERCENT = 50.0;  // Start stops after 50% completion
const int MAX_STOP_DELAY = 300;         // Maximum stop delay in ms
const int MIN_STOP_DELAY = 25;          // Minimum stop delay in ms
const int STOP_INTERVAL_LOOPS = 1;      // Apply stop every N loops when in stop zone


/* -------- Encoder Steps (ISR updated elsewhere) -------- */
volatile int32_t m1_steps = 0;
volatile int32_t m2_steps = 0;

// Button configuration

bool button_was_pressed = false;
unsigned long last_debounce_time = 0;
const unsigned long debounce_delay = 50; // 50ms is standard


volatile MotionState motionState = MS_IDLE;
#define uint long







#define  INIT_SP {0}




#define CURR_INT1 {0 }

#define CURR_INT {0 }


volatile CurrentState curr;


#define m1_pulses   (curr.total_pulse.m1)
#define m2_pulses   (curr.total_pulse.m2)

#define m1_pps   (curr.short_pps.m1)
#define m2_pps   (curr.short_pps.m2)

#define m1_pps_l   (curr.long_pps.m1)
#define m2_pps_l   (curr.long_pps.m2)


#define m1_pwm   (curr.pwm.m1)
#define m2_pwm   (curr.pwm.m2)


#define m1_pps_long   curr.long_term_pps.m1
#define m2_pps_long   curr.long_term_pps.m2

#define m1_pps_long2   curr.short_term_pps.m1
#define m2_pps_long2   curr.short_term_pps.m2

extern const char* formatToStaticBuffer(const char* format, ...);


gyroBegin(){
    curr.lastMicros = micros();
    curr.localTurn =0;
    //gyroUpdate();
  
}

gyroUpdate(float gyroZ){
   // curr.lastMicros = micros();
     unsigned long now = micros();
    float dt = (now - curr.lastMicros) * 1e-6;
     curr.lastMicros = now;

    float delta = gyroZ * dt;
     curr.localTurn  += delta;
     curr.globalTurn += delta;
}

gyroRBUpdate(float gyroZ){
   
     curr.localTurn  = gyroZ;
     curr.globalTurn = gyroZ;
}



#define tourTarget  curr.ideal_pos
#define robotPose  curr.current_pos
#define odoPose  curr.odo_pos
#define odoPoseLast  curr.odo_pos





volatile long m1_pulsesx = 0;
volatile long m2_pulsesx = 0;

volatile int m1_pwmx = 0;
volatile int m2_pwmx = 0;

volatile int m1_pwm_last = 0;
volatile int m2_pwm_last = 0;


volatile long m1_pulses_speed = 0;
volatile long m2_pulses_speed = 0;


volatile long m1_pulses_last = 0;
volatile long m2_pulses_last = 0;


volatile float m1_ppsx = 0;
volatile float m2_ppsx = 0;

volatile float m1_pps_lastx = 0;
volatile float m2_pps_lastx = 0;

volatile float m1_pps_accl = 0;
volatile float m2_pps_accl = 0;
volatile char cur_cmd  = ' ';
volatile int i  = -1;




// ---------- PID parameters ----------
volatile float m1_target_pps = 0;
volatile float m2_target_pps = 0;


float m1_Kp = 0.8;
float m1_Ki = 0.02;
float m1_Kd = 0.12;

// ---------- PID state ----------
float m1_pid_i = 0;
float m1_pid_last_err = 0;


float m2_Kp = 0.8;
float m2_Ki = 0.02;
float m2_Kd = 0.12;

// ---------- PID state ----------
float m2_pid_i = 0;
float m2_pid_last_err = 0;


// Limits
#define PWM_MIN2  0
#define PWM_MAX3  1000


// -------- Move command state --------
volatile long m1_move_start_pulses = 0;
volatile long m1_move_target_pulses = 0;
volatile bool m1_move_active = false;

// Debug / tracking
volatile long m1_move_current = 0;


volatile long m2_move_start_pulses = 0;
volatile long m2_move_target_pulses = 0;
volatile bool m2_move_active = false;

// Debug / tracking
volatile long m2_move_current = 0;


// -------- Robot pose --------


volatile float robot_heading_deg = 0.0;
volatile float robot_heading_deg_prev = 0.0;

// -------- Encoder tracking for odometry --------

volatile long m1_pulses_odo_last = 0;
volatile long m2_pulses_odo_last = 0;


char robotTour[] = "FSFS";
uint8_t tourIndex = 0;

/* ===================== TARGET MOVE (NEW) ================= */

struct MoveTarget {
    float x;
    float y;
    float heading;
    float totalDist;
};

MoveTarget moveTarget;



/* ===================== ARC STATE (NEW) =================== */

struct ArcState {
    float cx, cy;
    float radius;
    float curAngle;
    float stepAngle;
    int   stepsLeft;
    int   dir;
};

ArcState arc;

enum MotionState1 {
    MS_IDLE1,
    MS_MOVE_TO1,
    MS_ARC_TURN1,
    MS_SOFT_BRAKE111,
    MS_DONE1
};

MotionState1 motionState1 = MS_IDLE1;

/* ===================== HEADING PID (NEW) ================= */


/* ---- Heading PID ---- */
float hKp = 3.0f;
float hKi = 0.02f;
float hKd = 0.2f;

float h_i = 0;
float h_lastErr = 0;

/* ---- Distance PID (optional but useful) ---- */
float dKp = 1.0f;


/* ===================== UTILS (NEW) ======================= */

float NormalizeAngle2(float a)
{
    while (a > PI)  a -= TWO_PI;
    while (a < -PI) a += TWO_PI;
    return a;
}

/* ===================== HEADING PID (NEW) ================= */



/* ===================== S-CURVE SPEED (NEW) =============== */

float SCurve(float remaining, float total)
{
    float s = 1.0f - (remaining / total);
    s = constrain(s, 0, 1);
    return s * s * (3 - 2 * s);
}

#define PWM_DEADBAND 150
#define PWM_MAX_MOTER 1023


void setMotor1(int pwm)
{
    pwm = constrain(pwm, -PWM_MAX_MOTER, PWM_MAX_MOTER);
    curr.pwm.m1 = pwm;
    curr.pwm_m1 = pwm;
    
    uint16_t p = (uint16_t)abs(pwm);

    if (p < PWM_DEADBAND) {
        OCR4A = 0;
        OCR4B = 0;
        return;
    }

    if (pwm >= 0) {
        OCR4A = 0;
        OCR4B = p;
    } else {
        OCR4A = p;
        OCR4B = 0;
    }
}


void setMotor2(int pwm)
{
  /*
    pwm = constrain(pwm, -PWM_MAX_MOTER, PWM_MAX_MOTER);
    curr.pwm.m2 = pwm;
    curr.pwm_m2 = pwm;


    uint16_t p = (uint16_t)abs(pwm);

    if (p < PWM_DEADBAND) {
        OCR1A = 0;
        OCR1B = 0;
        return;
    }

    if (pwm >= 0) {
        OCR1A = p;
        OCR1B = 0;
    } else {
        OCR1A = 0;
        OCR1B = p;
    }*/
}






// ---------- Timer2 setup ----------
void setupSpeedTimer() {
    cli();
    TCCR2A = 0;
    TCCR2B = 0;
    TCCR2A |= (1 << WGM21);
    TCCR2B |= (1 << CS22) | (1 << CS20);
    // 125kHz / 125 = 1ms tick
    OCR2A = 124;
    TIMSK2 |= (1 << OCIE2A);
    sei();
}



void Motor1UpdateTargetPPS(float targetPPS, int rangeStart, int rangeEnd)
{
    
    // ---- Defaults ----
    if (rangeStart ==-1) rangeStart = 50;
    if (rangeEnd   ==-1) rangeEnd   = 320;
    if (rangeEnd < rangeStart) rangeEnd = rangeStart;
    m1_target_pps = targetPPS;
    // ---- Atomic read ----
    noInterrupts();
    float currentPPS = m1_pps;
    uint16_t currentPWM = m1_pwm;
    interrupts();

    // ---- PID error ----
    float err = targetPPS - currentPPS;

    if (abs(err) <= 20) err = 0;   // deadband

    // ---- Integral ----
    m1_pid_i += err;
    m1_pid_i = constrain(m1_pid_i, -3000, 3000);

    // ---- Derivative ----
    float dErr = err - m1_pid_last_err;
    m1_pid_last_err = err;

    // ---- PID output ----
    float pid =
        (m1_Kp * err) +
        (m1_Ki * m1_pid_i) +
        (m1_Kd * dErr);

    // ---- Requested PWM ----
    float requestedPWM = currentPWM + pid;

    // ---- Slew rate limit ----
    float minPWM = currentPWM - PWM_STEP_LIMIT;
    float maxPWM = currentPWM + PWM_STEP_LIMIT;

    float limitedPWM = constrain(requestedPWM, minPWM, maxPWM);

    // ---- Absolute & range clamp ----
    limitedPWM = constrain(limitedPWM, rangeStart, rangeEnd);

    setMotor1((uint16_t)limitedPWM);
}


void Motor2UpdateTargetPPS(float targetPPS, int rangeStart, int rangeEnd)
{

    // ---- Defaults ----
    if (rangeStart <= 0) rangeStart = 50;
    if (rangeEnd   <= 0) rangeEnd   = 320;
    if (rangeEnd < rangeStart) rangeEnd = rangeStart;

    m2_target_pps = targetPPS;

    // ---- Atomic read ----
    noInterrupts();
    float currentPPS = m2_pps;
    uint16_t currentPWM = m2_pwm;
    interrupts();

    // ---- PID error ----
    float err = targetPPS - currentPPS;

    if (abs(err) < 10) err = 0;

    if (err ==0) return;

    // ---- Integral ----
    m2_pid_i += err;
    m2_pid_i = constrain(m2_pid_i, -3000, 3000);

    // ---- Derivative ----
    float dErr = err - m2_pid_last_err;
    m2_pid_last_err = err;

    // ---- PID output ----
    float pid =
        (m2_Kp * err) +
        (m2_Ki * m2_pid_i) +
        (m2_Kd * dErr);

    // ---- Requested PWM ----
    float requestedPWM = currentPWM + pid;

    // ---- Slew rate limit ----
    float minPWM = currentPWM - PWM_STEP_LIMIT;
    float maxPWM = currentPWM + PWM_STEP_LIMIT;

    float limitedPWM = constrain(requestedPWM, minPWM, maxPWM);

    // ---- Absolute & range clamp ----
    limitedPWM = constrain(limitedPWM, rangeStart, rangeEnd);

    setMotor2((uint16_t)limitedPWM);
}


void MoveMotor1Pulses(
    long noOfPulseSteps,
    float initialTargetPPS,
    float minTargetPPS,
    float maxTargetPPS,
    int pwmRangeStart,
    int pwmRangeEnd
)
{
    // ---- Initialize move ----
    noInterrupts();
    m1_move_start_pulses  = m1_pulses;
    m1_move_target_pulses = noOfPulseSteps;
    interrupts();

    m1_move_active = true;

    // ---- Safety ----
    if (minTargetPPS < 10) minTargetPPS = 10;
    if (maxTargetPPS < minTargetPPS) maxTargetPPS = minTargetPPS;
    if (initialTargetPPS > maxTargetPPS) initialTargetPPS = maxTargetPPS;

    // ---- Control loop ----
    while (m1_move_active)
    {
        // Run at PPS update rate
        static unsigned long lastUpdate = 0;
        if (millis() - lastUpdate < SAMPLE_MS_PPS)
            continue;

        lastUpdate = millis();

        // ---- Read encoder atomically ----
        noInterrupts();
        long currentPulses = m1_pulses;
        interrupts();

        long moved = currentPulses - m1_move_start_pulses;
        long remaining = m1_move_target_pulses - moved;

        m1_move_current = moved;

        // ---- Stop condition ----
        if (remaining <= 0)
        {
            setMotor1(0);
            m1_move_active = false;

            LOG_INFOLN("M1 MOVE COMPLETE");
            break;
        }

        // ---- Distance → Target PPS (ramp down) ----
        // As remaining pulses shrink, PPS reduces
        float targetPPS;

        if (remaining > (m1_move_target_pulses * 0.4))
        {
            // Far from target → cruise
            targetPPS = initialTargetPPS;
        }
        else
        {
            // Close → proportional slowdown
            targetPPS = map(
                remaining,
                0,
                m1_move_target_pulses * 0.4,
                minTargetPPS,
                initialTargetPPS
            );
        }

        targetPPS = constrain(targetPPS, minTargetPPS, maxTargetPPS);

        // ---- Call your existing PID ----
        Motor1UpdateTargetPPS(targetPPS, pwmRangeStart, pwmRangeEnd);

    }
}


void MoveMotor2Pulses(
    long noOfPulseSteps,
    float initialTargetPPS,
    float minTargetPPS,
    float maxTargetPPS,
    int pwmRangeStart,
    int pwmRangeEnd
)
{
    // ---- Initialize move ----
    noInterrupts();
    m2_move_start_pulses  = m2_pulses;
    m2_move_target_pulses = noOfPulseSteps;
    interrupts();

    m2_move_active = true;

    // ---- Safety ----
    if (minTargetPPS < 10) minTargetPPS = 10;
    if (maxTargetPPS < minTargetPPS) maxTargetPPS = minTargetPPS;
    if (initialTargetPPS > maxTargetPPS) initialTargetPPS = maxTargetPPS;

    // ---- Control loop ----
    while (m2_move_active)
    {
        // Run at PPS update rate
        static unsigned long lastUpdate = 0;
        if (millis() - lastUpdate < SAMPLE_MS_PPS)
            continue;

        lastUpdate = millis();

        // ---- Read encoder atomically ----
        noInterrupts();
        long currentPulses = m2_pulses;
        interrupts();

        long moved = currentPulses - m2_move_start_pulses;
        long remaining = m2_move_target_pulses - moved;

        m2_move_current = moved;

        // ---- Stop condition ----
        if (remaining <= 0)
        {
            setMotor1(0);
            m2_move_active = false;

            LOG_INFOLN("M1 MOVE COMPLETE");
            break;
        }

        // ---- Distance → Target PPS (ramp down) ----
        // As remaining pulses shrink, PPS reduces
        float targetPPS;

        if (remaining > (m2_move_target_pulses * 0.4))
        {
            // Far from target → cruise
            targetPPS = initialTargetPPS;
        }
        else
        {
            // Close → proportional slowdown
            targetPPS = map(
                remaining,
                0,
                m2_move_target_pulses * 0.4,
                minTargetPPS,
                initialTargetPPS
            );
        }

        targetPPS = constrain(targetPPS, minTargetPPS, maxTargetPPS);

        // ---- Call your existing PID ----
        Motor2UpdateTargetPPS(targetPPS, pwmRangeStart, pwmRangeEnd);

       
    }
}

extern void UpdateRobotOdometry();

ISR(TIMER2_COMPA_vect)
{
    static uint16_t ms_short = 0;
    static uint16_t ms_long  = 0;

    ms_short++;
    ms_long++;

    const uint16_t SHORT_MS = 25;
    const uint16_t LONG_MS  = 100;

    /* ---------- SHORT WINDOW (25 ms) ---------- */
    if (ms_short >= SHORT_MS) {
        ms_short = 0;

        long m1 = curr.total_pulse.m1;
        long m2 = curr.total_pulse.m2;

        long dp1 = m1 - curr.last_short_pulse.m1;
        long dp2 = m2 - curr.last_short_pulse.m2;

        float prev_pps1 = curr.short_pps.m1;
        float prev_pps2 = curr.short_pps.m2;

        curr.short_pps.m1 = dp1 * (1000.0f / SHORT_MS);
        curr.short_pps.m2 = dp2 * (1000.0f / SHORT_MS);

        curr.short_accel.m1 =
            (curr.short_pps.m1 - prev_pps1) * (1000.0f / SHORT_MS);

        curr.short_accel.m2 =
            (curr.short_pps.m2 - prev_pps2) * (1000.0f / SHORT_MS);

        curr.last_short_pulse.m1 = m1;
        curr.last_short_pulse.m2 = m2;
        //#if 
        UpdateRobotOdometry();
    
    }

    /* ---------- LONG WINDOW (100 ms) ---------- */
    if (ms_long >= LONG_MS) {
        ms_long = 0;

        long m1 = curr.total_pulse.m1;
        long m2 = curr.total_pulse.m2;

        long dp1 = m1 - curr.last_long_pulse.m1;
        long dp2 = m2 - curr.last_long_pulse.m2;

        curr.long_pps.m1 = dp1 * (1000.0f / LONG_MS);
        curr.long_pps.m2 = dp2 * (1000.0f / LONG_MS);

        curr.last_long_pulse.m1 = m1;
        curr.last_long_pulse.m2 = m2;

        /* Long window = best place for odometry */
        
    }
}

void resetBoost(){

curr.halt.m1_halt_count = 0;
curr.halt.m2_halt_count = 0;
curr.halt.m1_boost = 0;
curr.halt.m2_boost = 0;




}


class TurnTracker {
public:
  void begin() {
    curr.lastMicros = micros();
  }

  void update(float gyroZ) {
    gyroUpdate(gyroZ);
  }

  float getLocal()  const { return curr.localTurn; }
  float getGlobal() const { return curr.globalTurn; }
  void resetLocal() { curr.localTurn = 0.0; }

};
void applyBreak(){
  OCR4A = 1023 ; OCR4B = 1023;      
  OCR1A = 1023; OCR1B = 1023;
}

TurnTracker turnTracker;
void resetLocalGyro(){
curr.localTurn = 0.0;
}





void StopMotors(){
  setMotor1(0);
  setMotor2(0);
  
}

void StopMotorsTime(
    uint32_t common_us,
    uint32_t m1_us,
    uint32_t m2_us,
    int p_m1_pwm,
    int p_m2_pwm
) {
    uint32_t t0 = micros();
    uint32_t t;

    // Stop both motors immediately
    setMotor1(0);
    setMotor2(0);

    uint32_t end_time = common_us;
    if (m1_us > end_time) end_time = m1_us;
    if (m2_us > end_time) end_time = m2_us;

    bool m1_started = false;
    bool m2_started = false;

    while (1) {
        t = micros() - t0;

        // Common stop time
        if (t < common_us) {
            setMotor1(0);
            setMotor2(0);
        }
        else {
            // Motor 1
            if (!m1_started && t >= m1_us) {
                setMotor1(p_m1_pwm);
                m1_started = true;
            }

            // Motor 2
            if (!m2_started && t >= m2_us) {
                setMotor2(p_m2_pwm);
                m2_started = true;
            }
        }

        // Exit after max(m1_us, m2_us)
        if (t >= end_time)
            break;
    }
}

long lastPrintTime=0;

void  printDebugStatusBleMove(){

    LOG_INFO3("S" , m1_pps ,m2_pps  );    
    LOG_INFO3("W" , m1_pwm , m1_pwm  ); 
    LOG_INFO3("E" , m1_pwm , m1_pwm  ); 
    
    Serial.println("");


}

void  printDebugStatusOld(){
  
  //if (motionState != MS_MOVE_TO) return;
 // return;

 #ifndef DEBUG 
    return;
 #endif 
  return;

  if (millis()>9000) return;
   static uint32_t last = 0;
   last++;
   if (last%5==0){

    //Serial.println("--------------");



    Serial.print(" Counter: ");
    Serial.print(last);

    Serial.print(" Millis: ");
    Serial.print(millis());

    
    LOG_INFO3(" Remaining Pulse M1/M2: " , curr.remaining_pulse_m1 , curr.remaining_pulse_m2  );
       

    Serial.print(" Tour Current Cmd ");
    Serial.print(cur_cmd);

    Serial.print(" tourIndex : ");
    Serial.print( tourIndex );

   LOG_INFO3(" Ideal Target x/y:" , tourTarget.x ,tourTarget.y  );

   Serial.print(" heading: ");
   Serial.print(tourTarget.heading);
   LOG_INFO3(" Move Target x/y:" , moveTarget.x ,moveTarget.y  );




   
    Serial.print(" heading: ");
    Serial.print(moveTarget.heading);

    Serial.print(" totalDist: ");
    Serial.print( moveTarget.totalDist );


    Serial.print(" Robot Pose : heading ");
    Serial.print(robotPose.heading);
    Serial.print(" Robot Pose : distPulse ");
    Serial.print(robotPose.distPulse);

    LOG_INFO3(" robotPose Actual x/y:" , robotPose.x ,robotPose.y  );
    LOG_INFO3(" PPS M1/m2:" , m1_pps ,m2_pps  );    
    LOG_INFO3(" PWM: M1/M2" , m1_pwm , m1_pwm  ); 


    Serial.println(" ");
   }
  
}

void StopMotorsTemp(int _delay) {
  setMotor1(0);
  setMotor2(0);
  
  delay(_delay);
  DEBUG_PRINT("Motors stopMotorsTemp for stopped: ");
  LOG_INFOLN(_delay);  

}

