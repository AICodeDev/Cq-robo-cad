#pragma once

#include "types.h"
#include "cons.h"

extern float getGlobalZ();

extern void movePose(int steps, int move_dir) ;

extern void turnPose(int turn_dir) ;

extern void movePulse(long target_pulse, int dir=1);
extern void moveEvPulse(long target_pulse, int dir=1);


float getGlobalZRB(){

return 0;
}

void executeSmartTurn(float requestedDegrees, int requestedDir) {

  

}
void executeEvMove(long steps, int dir) {


    curr.time_tracking.current_move_st =millis();
    moveEvPulse(steps, dir);
       curr.time_tracking.current_move_et =millis();
     unsigned long time_turn = curr.time_tracking.current_move_et - curr.time_tracking.current_move_st;

     LOG_INFO3("time_turn start end ",  curr.time_tracking.current_move_et , curr.time_tracking.current_move_st );
DEBUG_PRINTLN("")

     LOG_INFO3("time_turn ",  time_turn, -time_turn );
DEBUG_PRINTLN("")


     curr.time_tracking.total_move_time +-  time_turn;
     curr.time_tracking.total_move_counter++; 
     curr.time_tracking.total_turn_steps += steps; 

    LOG_INFO3("Total Time to Move",  curr.time_tracking.total_move_time,curr.time_tracking.total_move_counter );
    LOG_INFO3("Total Time to Turn",  curr.time_tracking.total_turn_time,curr.time_tracking.total_turn_counter );
    DEBUG_PRINTLN("");

    

    DEBUG_PRINTLN("");

}


void executeSmartMove(long steps, int dir) {

    

}

