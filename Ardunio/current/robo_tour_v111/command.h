#pragma once;
#include "cons.h"
//LWRELERWLWRWLWRWLWRW
// LW RW 
//String moveCommands = "W  LW RW  LW RW ";
//2500.2700 .2670ms.2635 for move
//1.3 to 1.4 second for turn

String moveCommands = "";


extern void movePulse(long target_pulse, int dir=1);
extern void turnLeftOfRight90(float degree=89 , int dir = 1 );
extern void turnLeftOfRight90Icm(float degree=89 , int dir= 1 );

extern void executeSmartTurn(float requestedDegrees, int requestedDir);
//extern void executeSmartTurn(float requestedDegrees, int requestedDir);
extern void executeSmartMove(long steps, int dir);

void moveForward(){

    movePulse(FULL_PULSE + EXTRA_FULL_PULSE ,1);
    delay(50);


}
void movePose(int steps, int move_dir) {
    
  //  curr.prev_ipose_move = curr.ipose ;
  //  curr.prev_ipose = curr.ipose ;
    

    // move_dir: 1 is Forward, -1 is Reverse
    curr.ipose.x_pos += (steps * curr.ipose.x_dir * move_dir);
    curr.ipose.y_pos += (steps * curr.ipose.y_dir * move_dir);
}

void turnPose(int turn_dir) {

//  curr.prev_ipose_turn = curr.ipose ;
//  curr.prev_ipose = curr.ipose ;
  


    // Save current directions to temporary variables
    int old_x = curr.ipose.x_dir;
    int old_y = curr.ipose.y_dir;

    if (turn_dir == 1) { // 90 Degrees RIGHT
        curr.ipose.x_dir = old_y;
        curr.ipose.y_dir = -old_x;
    } 
    else if (turn_dir == -1) { // 90 Degrees LEFT
        curr.ipose.x_dir = -old_y;
        curr.ipose.y_dir = old_x;
    }

    // Update the heading numeric value for your tracking (-180 to 180)
    curr.ipose.prev_heading = curr.ipose.heading;
    curr.ipose.heading += (turn_dir * 90);

    // Keep heading in range [-180, 180]
    if (curr.ipose.heading > 180)  curr.ipose.heading -= 360;
    if (curr.ipose.heading <= -180) curr.ipose.heading += 360;
    if (curr.ipose.heading == -180) curr.ipose.heading =180;

}










// --- Move Command Execution ---

// --- Define Your Actions Below ---

void moveForward5Cm() {
  // Add motor logic to move 25cm
  // movePulse( HALF_PULSE + EXTRA_HALF_PULSE ,1);
  executeSmartMove( FULL_PULSE/4 , 1);
  delay(50);

}

void moveForward25Cm() {
  // Add motor logic to move 25cm
  // movePulse( HALF_PULSE + EXTRA_HALF_PULSE ,1);
   executeSmartMove( FULL_PULSE/2 , 1);
  

    delay(50);
}

void moveForward50Cm() {
  executeSmartMove(FULL_PULSE + 0 , 1);
  
  //movePulse( FULL_PULSE + EXTRA_FULL_PULSE ,1);
  delay(50);

  // Add motor logic to move 50cm
}

void moveForward75Cm() {
  executeSmartMove(FULL_PULSE + HALF_PULSE , 1);

 // movePulse( FULL_PULSE + HALF_PULSE + EXTRA_FULL_PULSE ,1);
  delay(50);


  // Add motor logic to move 75cm
}

void moveForward100Cm() {
  // Add motor logic to move 100cm
 executeSmartMove(FULL_PULSE *2 , 1);
 // movePulse( FULL_PULSE + FULL_PULSE + EXTRA_FULL_PULSE  ,1);
  delay(50);


}

void moveForward150Cm() {
  
  movePulse( FULL_PULSE*3 + EXTRA_FULL_PULSE   ,1);
  delay(50);

  // Add motor logic to move 150cm
}

void turnRight90() {
  // Add motor logic for a 90-degree right turn
  
  #if USE_ICM_GYRO
    executeSmartTurn(MY_90,1);
    //turnLeftOfRight90Icm(MY_90,1);
  #else
    
    executeSmartTurn(MY_90,1);
    
  #endif

}

void turnLeft90() {

  
   #if USE_ICM_GYRO 
    //turnLeftOfRight90Icm(MY_90,-1);
     executeSmartTurn(MY_90,-1);
  #else

    executeSmartTurn(MY_90,-1);

  #endif


}

void reverse25() {
  // Add motor logic to back up 25cm
  Serial.println("REv");
  executeSmartMove(HALF_PULSE , -1);

}
void executeCommand(char cmd) {
  switch (cmd) {
    case '+':  curr.global_direction = 1;  break;
    case '-':  curr.global_direction = -1;  break;   
    
    case '1':  executeSmartMove(PULSE_PER_CM * 10 , curr.global_direction);  break;
    case '2':  executeSmartMove(PULSE_PER_CM * 20 , curr.global_direction);  break;
    case '3':  executeSmartMove(PULSE_PER_CM * 30 , curr.global_direction);  break;
    case '4':  executeSmartMove(PULSE_PER_CM * 40 , curr.global_direction);  break;
    case '5':  executeSmartMove(PULSE_PER_CM * 50 , curr.global_direction);  break;
    case '6':  executeSmartMove(PULSE_PER_CM * 60 , curr.global_direction);  break;
    case '7':  executeSmartMove(PULSE_PER_CM * 70 , curr.global_direction);  break;
    case '8':  executeSmartMove(PULSE_PER_CM * 80 , curr.global_direction);  break;
    case '9':  executeSmartMove(PULSE_PER_CM * 90 , curr.global_direction);  break;
    case '0':  executeSmartMove(PULSE_PER_CM * 100 , curr.global_direction);  break;
    
    
    
    
    
    
    
    
    
    
    case 'W': delay(500);  break;
    
    
    case 'F': moveForward50Cm();  break;
    case 'R': turnRight90();      break;
    case 'L': turnLeft90();       break;
    case 'H': moveForward25Cm();  break;
    case 'D': moveForward100Cm(); break;
    case 'T': moveForward150Cm(); break;      
    case 'B': 
    case 'b': 
    reverse25();        break;
    case 'O': reverse25();        break;
    
    // Note: Removed duplicate 'R' case to prevent compiler errors
    
    default:  /* Ignore unknown characters */ break; 
  }
}

void excuteCommmandAll(){
  curr.error_tracking ={0};
  curr = {0};
  curr.global_direction=1;

  // float oldLocalZ = gyro.updateZ();
  // delay(50);
  // oldLocalZ = gyro.updateZ();
  // DEBUG_PRINTLN(oldLocalZ);
  for (int i = 0; i < moveCommands.length(); i++) {
    char cmd = moveCommands[i]; // Get one letter at a time
    executeCommand(cmd);
    delay(200);  
  }  // 4. Brief delay so the robot doesn't jerk between moves
  delay(200); 
  

}

