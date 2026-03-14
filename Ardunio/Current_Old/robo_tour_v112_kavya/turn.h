#include "Arduino.h"
//#include "RB_QMIND_PLUS.h"
#include "RB_GYRO_FAST.h"
#include "SafeLogger.h"
#include "debug_macro.h"

extern SafeBleLogger bleLogger;
extern void resetPulse();

float getGlobalZ(){
  float f=0;
  return f;

}

float getLocalZ(){
  float f=0;
  return f;

}

void NextTurnStart(float target_angle, int dir) {

  //DEBUG_PRINT("NextTurnStart:") ;
  //DEBUG_PRINT(target_angle) ;
 // LOG_INFOLN("--------NextTurnStart:") ;
  resetPulse();

   //todo accumulate and adjst previous errors
      gyroBegin();
    //store and adjust last error;

      resetBoost();

      resetPulse();
   
        curr.localTurn = 0.0;
        curr.globalTurn = 0.0;
         #if USE_RB_GYRO_FAST
          gyro.resetLocal();
        #endif

        // curr.current_pulse.m1 = 0;
        // curr.current_pulse.m1 = 0;

        // curr.total_pulse.m1 = 0;
        // curr.total_pulse.m2 = 0;
        
        //curr.start_pulse.m1 = curr.total_pulse.m1;
        //curr.start_pulse.m2 = curr.total_pulse.m2;
        
   // interrupts();


  //  curr.target_pulse = target_pulse; 
    
    //curr.gryo_start = updateGyro();
    
    curr.target_angle = target_angle; //todo adjust gyro error from previus step

    //curr.gryo_current = curr.gryo_start;
    curr.error = target_angle;
    curr.turn_dir = dir;
    curr.loop_count = 0;
    curr.turn_start_ms = millis();
    
    //store and adjust last error;
    //reset local turn;
    curr.localTurn=0;
      
      m2_integral = 0;
      m2_previous_error = 0;

}

bool UpdateTurnState() {
    curr.loop_count++;


    curr.curr_m1_pulse = curr.CurrentM1Count();
    curr.curr_m2_pulse = curr.CurrentM2Count() ;
    
    // Timeout check
    if (millis() - curr.turn_start_ms > 8000) {
        DEBUG_PRINTLN("Turn timeout!");
        return false;
    }
    long total= curr.CurrentM1Count() +  curr.CurrentM2Count(); //245 + 245 is 90 degree
    float turnedBasedOnEncoder = total *  (( MY_90  * 1.0f) / (MY_90_PULSE * 1.0f));

    float turnedBasedonGyro=  abs(updateGyro());//current local angle
    float turned = abs(turnedBasedonGyro); 

   // float turned;

    float differenceThreshold = 15.0f; // Degrees of difference allowed before ignoring gyro
    float diff= turnedBasedOnEncoder - turnedBasedonGyro;
    diff = abs(diff);
    if (diff > differenceThreshold) {
        // Gyro is acting abnormal, trust the encoders
    //    LOG_INFO4("E: G/E ", turnedBasedonGyro ,  turnedBasedOnEncoder ,"\n" )
       
        turned = abs(turnedBasedOnEncoder);
    } else {
        // Gyro seems healthy, trust the gyro (usually more accurate for rotation)
        turned = turnedBasedonGyro;
     //   LOG_INFO4("G: G/E ", turnedBasedonGyro ,  turnedBasedOnEncoder ,"\n" )
       

    }



    curr.error = curr.target_angle - turned;
     curr.time_tracking.current_turn_et =millis();
    unsigned long time_turn = curr.time_tracking.current_turn_et - curr.time_tracking.current_turn_st;
    curr.time_tracking.turn_clock=time_turn;

    #if DEDUG 
     // PrintGyro();
    #endif 
   


 static  char buffer[128];



    // Done?
    if (abs(curr.error) <=TURN_TOLERENCE ) {
        #if DEBUG_BLE
//          Serial.print( ("gyro reache G %0.2f TURN %0.2f Error %0.2f  total %ld m1 %ld m2 %ld ", turnedBasedonGyro, abs(curr.error), (TURN_TOLERENCE) , abs(total) , curr.CurrentM1Count() , curr.CurrentM2Count() );
          Serial.print("Gyro T: ");
          
          Serial.print(turnedBasedonGyro);

          Serial.print("Enco T: ");
          
          Serial.print(turnedBasedOnEncoder);

          Serial.print(" Err Grro: ");
          
          Serial.print(curr.error);

          Serial.print(" Dir: ");
          
          Serial.print(curr.turn_dir);


          Serial.print(" Total: ");
          
          Serial.print(total);

          //curr.turn_dir

          Serial.println("--");

        //  snprintf(buffer, sizeof(buffer), " gyro reache   total %ld m1 %ld m2 %ld ", abs(total) , curr.CurrentM1Count() , curr.CurrentM2Count());

         // Serial.println(buffer);

        #endif

        
        return false;
    }
    
    if (abs(total)>(MY_90_PULSE_MAX) ){
     #if DEBUG_BLE
//          Serial.print( ("gyro reache G %0.2f TURN %0.2f Error %0.2f  total %ld m1 %ld m2 %ld ", turnedBasedonGyro, abs(curr.error), (TURN_TOLERENCE) , abs(total) , curr.CurrentM1Count() , curr.CurrentM2Count() );
          Serial.print("Gyro T: ");
          
          Serial.print(turnedBasedonGyro);

          Serial.print("Enco T: ");
          
          Serial.print(turnedBasedOnEncoder);

          Serial.print(" Err Grro: ");
          
          Serial.print(curr.error);

          Serial.print(" Total: ");
          
          Serial.print(total);

          
          Serial.println("--");

        //  snprintf(buffer, sizeof(buffer), " gyro reache   total %ld m1 %ld m2 %ld ", abs(total) , curr.CurrentM1Count() , curr.CurrentM2Count());

         // Serial.println(buffer);

        #endif


       return false;

    }

    return true;
}
void applyTurnBoost(){
      int short_pps_m1 = curr.short_pps.m1;
      int short_pps_m2 = curr.short_pps.m2;

      // -------- Motor 1 --------
      if (short_pps_m1 < PPS_HALT_THRESH &&
          curr.remaining_pulse_m1 > MIN_REMAINING_PULSE)
      {
          curr.halt.m1_halt_count++;
          if (curr.halt.m1_halt_count >= HALT_COUNT_TRIGGER) {
              curr.halt.m1_boost += BOOST_STEP;
              curr.halt.m1_boost = min(curr.halt.m1_boost, BOOST_MAX);
              curr.halt.m1_halt_count = HALT_COUNT_TRIGGER;
          }
      }
      else {
          curr.halt.m1_halt_count = 0;
          curr.halt.m1_boost -= BOOST_DECAY;
          if (curr.halt.m1_boost < 0) curr.halt.m1_boost = 0;
      }

      // -------- Motor 2 --------
      if (short_pps_m2 < PPS_HALT_THRESH &&
          curr.remaining_pulse_m2 > MIN_REMAINING_PULSE)
      {
          curr.halt.m2_halt_count++;
          if (curr.halt.m2_halt_count >= HALT_COUNT_TRIGGER) {
              curr.halt.m2_boost += BOOST_STEP;
              curr.halt.m2_boost = min(curr.halt.m2_boost, BOOST_MAX);
              curr.halt.m2_halt_count = HALT_COUNT_TRIGGER;
          }
      }
      else {
          curr.halt.m2_halt_count = 0;
          curr.halt.m2_boost -= BOOST_DECAY;
          if (curr.halt.m2_boost < 0) curr.halt.m2_boost = 0;
      }


}


void PrintGyroStat(){
 Serial.print("--");    
#ifdef DEBUG
      float z=  updateGyro();//current local angle

      String msg = "FT:" ; 
      //msg += String(curr.loop_count); 
     // msg += String(" "); 
      msg += String(abs(z)); 
      msg += String("-");
      msg += String(int(curr.CurrentM1Count() + curr.CurrentM2Count()) ); 
      msg += String("\n"); 
      ; 
      delay(100);
      bleLogger.print(msg);
     
            


#endif

}

void PrintGyroAll(){
return;
#ifdef DEBUG_BLE
            float z=  updateGyro();//current local angle

      String msg = "-GL " ; 
      msg += String(curr.loop_count); 
      msg += String(" A ");   
      msg += String(z); 
      msg += String(" E ");   
      msg += String(curr.pwm.m1); 
      msg += String(" ");     
      msg += String(curr.pwm.m2); 
      msg += String(" S "); 
      msg += String(int(curr.short_pps.m1)); 
      msg += String("/"); 
      msg += String(int(curr.short_pps.m2)); 
      msg += String(" ");
      msg += String(" M1/M2 "); 
      msg += String(int(curr.CurrentM1Count())); 
      msg += String("/"); 
      msg += String(int(curr.CurrentM2Count())); 
      msg += String(" ");


      msg += String(int( curr.heading_gyro));
  


      msg += String("\n"); 
      ; 
      
      bleLogger.print(msg);
              
            


#endif



}
#if USE_RB_GYRO_FAST
extern RB_GYRO_FAST   gyro;
 #endif 
void turnLeftOfRight90(float degree =89, int dir=1) {
 
  #if USE_RB_GYRO_FAST
      gyro.resetLocal();
  #endif 

  
    DEBUG_PRINTLN("=== GYRO TURN START ===");
    NextTurnStart(degree, dir); //4.5 Pulase per degree (only one wheel was moving)395 pulse for m2

    //stop  
    setMotor1(0);
    setMotor2(0);
    delay(5);
    
    int startPwm = (dir <0)? 320 : 300;

#if BLUE_WHEEL 
    startPwm = (dir <0)? 299 : 280;
#endif

    int overSpeedPwm = -1;
    int underSpeedPwm = -1;

    //warm up
    setMotor1(250* dir);
    setMotor2(-250 *dir);
    delay(10);
    
    
    //Start up
    
    setMotor1(startPwm * dir);
    setMotor2(-startPwm * dir);
    delay(20);
    

    const float START_REDUCING_AT = 60.0;  // Start slowing down at 40°
    
    while (UpdateTurnState()) {
        curr.loop_count++;
        applyTurnBoost();
        // Trapezoid speed based on remaining angle
        int calcPwm = startPwm + overSpeedPwm + underSpeedPwm ;
        int basePWM = TrapezoidSpeedForGyro(calcPwm, curr.error, START_REDUCING_AT);
        
        // Position correction between motors
        long pos_error = curr.CurrentM1Count() - curr.CurrentM2Count();
        int m2_adjust = constrain(pos_error * 4, -100, 100) * 1;
        
        int m1_speed_pwm = basePWM + curr.halt.m1_boost;
        int m2_speed_pwm = basePWM + m2_adjust + curr.halt.m2_boost;
        
        setMotor1(m1_speed_pwm * dir);
        setMotor2(-m2_speed_pwm * dir);
        float p1=m1_speed_pwm * dir;
        float p2= -m2_speed_pwm * dir;
        #if DEBUG
          if (curr.loop_count % 10==0){
            PrintGyroAll();
          }
        #endif 

      if ( (curr.short_pps.m1+curr.short_pps.m2) >=1200 ){
          StopMotors();
          delay(2);
          overSpeedPwm = overSpeedPwm-10;

      }
      else{
        overSpeedPwm = 0;
      }


      if ((curr.short_pps.m1 + curr.short_pps.m2) <=200 
      //&& curr.avg_remaining<300   
      )
      {
         underSpeedPwm = underSpeedPwm+40;
      }
      else if ((curr.short_pps.m1 + curr.short_pps.m2) <=100 
      //&& curr.avg_remaining<300   
      ){
        //underspeed Pwm
          underSpeedPwm = underSpeedPwm+25;

      }
      else{
        underSpeedPwm=0;
      }


        delay(8);
        StopMotors();

        if ( curr.loop_count %10 ==0){
            delay(2);
        }
        else{
          delay(1);
          delayMicroseconds(250);
        }
    
    
    }
    PrintGyroAll();
    StopMotors();
    ApplyBrake(250);


    float final_turned = updateGyro();;
    curr.error=curr.target_angle-final_turned;
    DEBUG_PRINT2("Tar: ", curr.target_angle);
    DEBUG_PRINT2("° | Act: ", final_turned);
    DEBUG_PRINT2("° | Err: ", curr.error);
    DEBUG_PRINTLN("°");
   // LOG_INFO3("M1/M2 pulses", curr.curr_m1_pulse, curr.curr_m2_pulse);
    DEBUG_PRINTLN("");
    PrintGyroAll();

   



}


void turnLeftOfRight90Icm(float degree =72, int dir =1 ) {
  //issue identify halt condition and use boost 

  #if USE_RB_GYRO_FAST 
    //gyro.resetLocal();
   // gyroBegin();
  #endif
  
   // dir=-1;
    NextTurnStart(degree, dir); //4.5 Pulase per degree (only one wheel was moving)395 pulse for m2

    //stop  
    setMotor1(0);
    setMotor2(0);
    delay(5);
    
    int startPwm = (dir <0)? 285 : 275;
    int overSpeedPwm = -1;
    int underSpeedPwm = -1;

    //warm up
    setMotor1(200* dir);
    setMotor2(-200 *dir);
    delay(10);
    
    
    //Start up
    
    setMotor1(startPwm * dir);
    setMotor2(-startPwm * dir);
    delay(5);
    

    const float START_REDUCING_AT = 65.0;  // Start slowing down at 40°
    
    while (UpdateTurnState()) {
        curr.loop_count++;
        applyTurnBoost();
        // Trapezoid speed based on remaining angle
        int calcPwm = startPwm + overSpeedPwm + underSpeedPwm ;
        int basePWM = TrapezoidSpeedForGyro(calcPwm, curr.error, START_REDUCING_AT)*0.95;
        
        // Position correction between motors
        long pos_error = curr.CurrentM1Count() - curr.CurrentM2Count();
        int m2_adjust = constrain(pos_error * 6, -100, 100) * 1;
        
        int m1_speed_pwm = basePWM + curr.halt.m1_boost;
        int m2_speed_pwm = basePWM + m2_adjust + curr.halt.m2_boost;
        
        setMotor1(m1_speed_pwm * dir);
        setMotor2(-m2_speed_pwm * dir);
        float p1=m1_speed_pwm * dir;
        float p2= -m2_speed_pwm * dir;
        #if DEBUG
          if (curr.loop_count % 3==0){
            PrintGyroAll();
          }
        #endif 

      if ( (curr.short_pps.m1+curr.short_pps.m2) >=1200 ){
          StopMotors();
          delay(1);delayMicroseconds(500);
          overSpeedPwm = overSpeedPwm-15;

      }
      else if ( (curr.short_pps.m1+curr.short_pps.m2) >=1100 ){
          StopMotors();
          delayMicroseconds(500);
          overSpeedPwm = overSpeedPwm-5;

      }

      else{
        overSpeedPwm = 0;
      }


      if ((curr.short_pps.m1 + curr.short_pps.m2) <=200 
      //&& curr.avg_remaining<300   
      )
      {
         underSpeedPwm = underSpeedPwm+25;
      }
      else if ((curr.short_pps.m1 + curr.short_pps.m2) <=200 
      //&& curr.avg_remaining<300   
      ){
        //underspeed Pwm
          underSpeedPwm = underSpeedPwm+5;

      }
      else{
        underSpeedPwm=0;
      }


        #if USE_ICM_GYRO 

          delay(4);
          StopMotors();
          delay(1);

        #else
          delay(10);
          StopMotors();
        
        #endif

        if ( curr.loop_count %10 ==0){
            delay(1);
        }
    
    
    }
    
    StopMotors();
    ApplyBrake(250);
    ApplyBrake(100);
    delay(200);


    float final_turned = updateGyro();;
    DEBUG_PRINT2("°Act:", final_turned);
    DEBUG_PRINT2(" T:", curr.target_angle);
    
    //DEBUG_PRINT2("° | Final error: ", curr.error);
    DEBUG_PRINTLN("°");
   // LOG_INFO3("M1/M2 pulses", curr.curr_m1_pulse, curr.curr_m2_pulse);
    DEBUG_PRINTLN("");
    PrintGyroAll();
    delay(100);
   

}