#pragma once

#include "types.h"
#include "cons.h"

extern float getGlobalZ();

extern void movePose(int steps, int move_dir) ;

extern void turnPose(int turn_dir) ;

#if USE_RB_GYRO_FAST
//extern RB_GYRO_FAST   gyro;
#endif

extern void movePulse(long target_pulse, int dir=1);

float getGlobalZRB(){
#if USE_RB_GYRO_FAST
  gyro.updateZ();
  return gyro.getGlobalZ();
#endif
return 0;
}
/*
struct TimeTracking {
    unsigned long st;    // 0, 90, 180, 270
    unsigned long et;     
    
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
*/
void executeSmartTurn(float requestedDegrees, int requestedDir) {

  turnPose(requestedDir);

  float currentGyro =0;
  curr.time_tracking.current_turn_st =millis();


  #if USE_RB_GYRO_FAST
    // 1. Capture where we are vs where we should be
     currentGyro = getGlobalZRB();
    gyro.fastRefresh();
    gyro.resetLocal();
  #endif

   // curr.local_turn=0;
    
    // 2. Determine the "Real" error from the last move
    // Example: If at 2.0 degrees, ideal is 0.0, error is -2.0
    float last_move_error =  curr.error_tracking.heading_error;//curr.error_tracking.ideal_cardinal - currentGyro;
   // float newLocalZ = gyro.updateZ(); //current local
     
    last_move_error=0;

    curr.error_tracking.heading_error =0;
    #if USE_RB_GYRO_FAST
     gyro.resetLocal();
    #endif
    // 3. Update the global "Ideal" for the NEXT move
    // If we are at 0 and turn 90 Right (dir 1), next ideal is 90
    curr.error_tracking.ideal_cardinal += (requestedDegrees * requestedDir);

    if (curr.error_tracking.ideal_cardinal>360) curr.error_tracking.ideal_cardinal - 360;
    if (curr.error_tracking.ideal_cardinal<360) curr.error_tracking.ideal_cardinal + 360;
    
   // last_move_error=0;
    
    // 4. Calculate the adjusted turn magnitude
    // Example: 90 degrees requested + (-2.0 error) = 88.0 actual degrees
    float adjustedDegrees = requestedDegrees + (last_move_error * requestedDir *-1);

    // 5. Safety: If adjustment makes degrees negative, flip direction
    int finalDir = requestedDir;
    if (adjustedDegrees < 0) {
        adjustedDegrees = abs(adjustedDegrees);
        finalDir *= -1; // Reverse the turn direction
    }
   
   
    
    #if USE_ICM_GYRO 
    //turnLeftOfRight90Icm(MY_90,-1);
     //executeSmartTurn(MY_90,1);
      turnLeftOfRight90Icm(adjustedDegrees, requestedDir ); //(adjustedDegrees, requestedDir);
    #else
      turnLeftOfRight90(adjustedDegrees, requestedDir ); //(adjustedDegrees, requestedDir);
    
    #endif

    // 6. Execute using your specific function
    
     curr.error_tracking.heading_error =0;

     curr.time_tracking.current_turn_et =millis();
     unsigned long time_turn = curr.time_tracking.current_turn_et - curr.time_tracking.current_turn_st;

    //   LOG_INFO3("time_turn start end ",  curr.time_tracking.current_turn_et , curr.time_tracking.current_turn_st );
    //   DEBUG_PRINTLN("");

    //  LOG_INFO3("time_turn ",  time_turn, -time_turn );
    //   DEBUG_PRINTLN("");


     curr.time_tracking.total_turn_time = curr.time_tracking.total_turn_time + time_turn;
     curr.time_tracking.total_turn_counter++; 
     curr.time_tracking.total_turn_steps += 600; 
  
    //  LOG_INFO3("Total ",  curr.time_tracking.total_turn_time , curr.time_tracking.total_turn_counter );
    // DEBUG_PRINTLN("");
      delay(100);
     
      PrintGyroStat();
     



}



void executeSmartMove(long steps, int dir) {

    movePose(steps, dir);

    curr.time_tracking.current_move_st =millis();


    float oldLocalZ = 0;
    #if USE_RB_GYRO_FAST
      gyro.updateZ();
      gyro.resetLocal();
    #endif

    long adjustment = 0;
    float angle = curr.error_tracking.ideal_cardinal;

    // A. Pick the error based on current axis
    if (angle == 0 || angle == 180) {
        adjustment = curr.error_tracking.y_error;
        curr.error_tracking.y_error = 0;
    } else {
        adjustment = curr.error_tracking.x_error;
        curr.error_tracking.x_error = 0;
    }

    // B. Apply error to the steps
    // If we overshot last time, adjustment will be negative, reducing finalSteps
    long finalSteps = steps ;//+ adjustment;
    if (finalSteps < 0) finalSteps = 0; // Prevent negative distance

    // C. Move the robot
    movePulse(finalSteps, dir);

    // D. Update Global Position Tracker
    // We use the 'intended' steps to keep the grid perfect
    long moveDist = steps * dir; 
    if (angle == 0)         curr.error_tracking.target_y += moveDist;
    else if (angle == 90)   curr.error_tracking.target_x += moveDist;
    else if (angle == 180)  curr.error_tracking.target_y -= moveDist;
    else if (angle == 270)  curr.error_tracking.target_x -= moveDist;

    // E. Calculate new error for next time
    // Actual distance is where the encoders actually stopped
    long actualTotal = (curr.CurrentM1Count() + curr.CurrentM2Count()) / 2;
    
    if (angle == 0 || angle == 180) {
        curr.error_tracking.y_error = curr.error_tracking.target_y - (actualTotal * dir);
    } else {
        curr.error_tracking.x_error = curr.error_tracking.target_x - (actualTotal * dir);
    }

     float newLocalZ =0;
     #if USE_RB_GYRO_FAST
      gyro.updateZ();
     #endif 
     
     curr.error_tracking.heading_error = newLocalZ;
     LOG_INFO3 ("Heading Error TODO" , curr.error_tracking.heading_error,newLocalZ );
     DEBUG_PRINTLN ("");

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

    

    DEBUG_PRINTLN("")

}

