#pragma once

struct Pose {
    int x_pos = 0;
    int y_pos = 0;
    int x_dir = 0; // Starting direction (facing North)
    int y_dir = 1;
    int heading = 0; 
    int prev_heading=0;
};


struct State {
    int x_pos = 0;
    int y_pos = 0;
    int x_dir = 0; // Starting direction (facing North)
    int y_dir = 1;
    int heading = 0; 
    int prev_heading=0;
};

struct Command {
    char cmd;
    char type;
    int steps;
    int degree;
    int move_dir;
    int turn_dir;    
};



struct ErrorTracking {
    float ideal_cardinal;    // 0, 90, 180, 270
    float heading_error;     
    
    long target_x;           // Ideal global X in steps
    long target_y;           // Ideal global Y in steps
    long x_error;            // Carryover for X
    long y_error;            // Carryover for Y
};

struct TimeTracking {
    unsigned long st;    // 0, 90, 180, 270
    unsigned long et;     
    unsigned long move_clock;
    unsigned long turn_clock;
         
    
    
    unsigned long current_move_st;    // 0, 90, 180, 270
    unsigned long current_move_et;  

    unsigned long total_move_time;
    unsigned long total_move_steps;
    unsigned long total_move_counter;
    

    unsigned long current_turn_st;    // 0, 90, 180, 270
    unsigned long current_turn_et;  

    unsigned long total_turn_time;
    unsigned long total_turn_steps;
    unsigned long total_turn_counter;


};


enum MotionState {
    MS_IDLE,
    MS_MOVE_TO,
    MS_ARC_TURN,
    MS_SOFT_BRAKE,

    MS_TURN_IN_PLACE,
    MS_FOLLOW_ARC,
    MS_SOFT_BRAKE222,
    MS_DONE,
    MS_IDLE11,
//     MS_DONE

};

struct Speed {
    int m1;
    int m2;
    int m1_adjust;
    int m2_adjust;
    int m1_pos;
    int m2_pos;
    int pos_error;


};

struct Position {
    int x;
    int y;
    float heading;
    float prevHeading;
    float distPulse;


};

struct Halt {
    
    // Boost
    int m1_boost;
    int m2_boost;
    int m1_halt_count;
    int m2_halt_count;



};

struct Metric {
    int m1_pps;
    int m2_pps;
    
    int m1_accl;
    int m2_accl;
    
    float heading;



};
struct PID {
  float Kp;// = 3.0f;
  float Ki;// = 0.02f;
  float Kd;// = 0.2f;

  float i;// = 0;
  float lastErr;// = 0;
};



struct point {
  int x;
  int y;

};

struct Point {
  float x;
  float y;

};

struct Accel {
  float m1;
  float m2;

};

struct Pulse {
  long m1;
  long m2;

};

struct Pwm {
  int m1;
  int m2;

};

struct Pps {
  float m1;
  float m2;

};

#define uint long

struct CurrentState {

    long m1_total_pulse;
    long m2_total_pulse;
    int global_direction;
    
    uint m1_start;
    uint m2_start;


    uint left_over_m1_pulse;
    uint left_over_m2_pulse;
    
    uint target_pulse;
    uint dir;
    
    uint pwm_m1;
    uint pwm_m2;
    uint curr_m1_pulse; //travleed for current movement
    uint curr_m2_pulse;    

    uint remaining_pulse_m1;        
    uint remaining_pulse_m2;        // radians
    uint avg_remaining;   
    uint last_avg_remaining;   
         
    
    float heading_encoder;       
    float heading_gyro;        
    
    float gryo_start;   
    float gryo_current;
     
    float error;    
    unsigned long lastMicros ;;   
    int turn_dir;
  
    float localTurn  ;
    float globalTurn ;
    
    float target_angle;
    unsigned long turn_start_ms;
    bool hard_brake_done;
    int loop_count;
    
    // Speed tracking
    long m1_last_count;
    long m2_last_count;
    unsigned long last_speed_us;
    float m1_pps;
    float m2_pps;
    
    
    int turn_targert_pulse;
    int type;


    
    Speed speed;
    Pose ipose;
    Pose change_required;
    Pose actual_change ;
    Pose error_change ;
    Pose error_adjustment ;
    
    
    
    
    Pose prev_ipose_move;
    Pose prev_ipose_turn;
    Pose prev_ipose;
    
    
    
    Position ideal_pos;
    Position current_pos;
    Position last_pos;
    Position odo_pos;
    Position odo_pos_last;
    
    Halt halt;
    Metric short_metric;
    Metric long_metric;
    PID h_pid;
    
    Point velocity;
    Point longVelocity2;

    Accel accel;

    Accel short_accel;
    Accel long_accel;

    Pps short_pps;
    Pps long_pps;

    //Pulse last_pulse;
    Pulse start_pulse;
    Pulse total_pulse;
    Pulse current_pulse;
    Pulse remaining_pulse;
    

    Pulse last_short_pulse;
    Pulse last_long_pulse;
    
    Pwm pwm;
    Pwm last_pwm;
    
    ErrorTracking error_tracking;
    TimeTracking  time_tracking;

    long CurrentM1Count(){
      return current_pulse.m1;
    }
    
    long CurrentM2Count(){      
      return current_pulse.m2;
    }

};
