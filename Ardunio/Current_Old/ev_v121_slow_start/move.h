#include "Arduino.h"
#pragma once

extern DistanceSelector selector;

void ApplyBrake(int ms=500, int stopMsBefore =0 , int stopMsAfter=0)
{
  if (stopMsBefore>0){
      OCR4A = 0;
      OCR4B = 0;

      OCR1A = 0;
      OCR1B = 0;

      delay(stopMsBefore);



  }

OCR4A = 1023;
OCR4B = 1023;

OCR1A = 1023;
OCR1B = 1023;

delay(ms);


if (stopMsAfter>0){
      OCR4A = 0;
      OCR4B = 0;

      OCR1A = 0;
      OCR1B = 0;

      delay(stopMsAfter);



  }

}
void applyMoveBoost(){
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






void resetPulse(){
     curr.total_pulse = {0};
   curr.total_pulse.m1 = 0;
   curr.total_pulse.m2 = 0;
    



   
  curr.m1_start = curr.total_pulse.m1;
  curr.m2_start = curr.total_pulse.m2;

 // curr.start_pulse =  curr.total_pulse; //.m1;
  //curr.start_pulse.m2 = curr.total_pulse.m2;

  curr.current_pulse.m1 =0;
  curr.current_pulse.m2 =0;
  curr.current_pulse = {0};
   

}
void NextMove(long target_pulse, int dir=1)
{
  //adjust any error from previus accumulated error of turn or back or forward (mainly turn)
  //based on current heading update the ideal robot pose
  resetBoost();
  //to bre removed;
    
  resetPulse();


  curr.target_pulse = target_pulse; 
  curr.type =1; //1 mean straight
  curr.dir = dir;
  curr.gryo_start =0;
  curr.localTurn = 0.0;
  curr.gryo_start = 0.0;

//  resetLocalGyro();

}




int UpdateMoveStateEv()
{
    //adjust any error from previus accumulated error of turn or back or forward (mainly turn)

    long t1 = curr.total_pulse.m1 - curr.m1_start;
    long t2 = curr.total_pulse.m2 - curr.m2_start;
    long p = t1+t2;//only one will have value
  //  LOG_INFO3("TT xx",  t1 ,   t2);

    curr.curr_m1_pulse = curr.CurrentM1Count() + curr.CurrentM1Count();
    curr.curr_m2_pulse = curr.CurrentM1Count() + curr.CurrentM2Count();

    //LOG_INFO3("xx",  curr.curr_m1_pulse ,   curr.curr_m2_pulse);
    

    //DEBUG_PRINTLN("");


    curr.remaining_pulse.m1 = curr.target_pulse - p;
    curr.remaining_pulse.m2 = curr.target_pulse - p;
    curr.avg_remaining =
        (curr.remaining_pulse.m1 + curr.remaining_pulse.m2) * 0.5f;

    //LOG_INFO3("AVG ",  curr.avg_remaining  ,   -1);
    //DEBUG_PRINTLN("");

    if (curr.avg_remaining <71){
        if (curr.last_avg_remaining != curr.avg_remaining)
          {
              LOG_INFO3("Move : Low Balance: heading_error ",  curr.error_tracking.heading_error  ,  0);
              LOG_INFO3(" remaining_pulse ",  curr.remaining_pulse.m1  ,   curr.remaining_pulse.m2 );              
              DEBUG_PRINT2(" avg_remaining ",  curr.avg_remaining    );
              DEBUG_PRINTLN();
    
          }

    }

    curr.last_avg_remaining= curr.avg_remaining;

    return (curr.avg_remaining > 70 ? 1 : 0); // 70 is tolerance step
}



void PrintMove(){

    long r1=curr.target_pulse- (curr.current_pulse.m1 );
    long r2=  curr.target_pulse-  (curr.current_pulse.m1 );
      String msg = "PML N " ; 
      msg += String(curr.loop_count); 

      msg += " Time: " ; 
      msg += String(millis()); 
      

      msg += " Pulse: " ; 

      msg += String(curr.current_pulse.m1 + curr.current_pulse.m2); 
    
      msg += String(" PWN : "); 

      msg += String(curr.pwm.m1); 
    
      msg += String(" S-S: "); 
      msg += String(int(curr.short_pps.m1)); 
      
      msg += String(" "); 

      msg += String(" L_S: "); 
      msg += String(int(curr.long_pps.m1)); 
      
     
      msg += String(" Rem: "); 
      msg += String(r1); 
    

      msg += String("\n"); 
      ; 
      
      //bleLogger.print(msg);

      Serial.println(msg);

      //todo remove
      //delay(200);


}

// void moveEvPulsePendingSteps(long target_pulse, int dir)
// {
//     delay(2000);
//     Serial.println("moveEvPulse");
//     Serial.println(target_pulse);
//     PrintMove();

//     NextMove(target_pulse,dir);
//     PrintMove();
//     Serial.println("setup done moveEvPulse");
//     Serial.println(target_pulse);

//     curr.avg_remaining = target_pulse;

//     curr.halt.m1_boost=0;
//     curr.halt.m2_boost=0;
//     curr.halt.m1_halt_count=0;
//     curr.halt.m1_halt_count=0;
    
    

   

//     int startPwm = 800;
//     int overSpeedPwm = -1;
//     int underSpeedPwm = -1;
    
//     #if USE_RB_GYRO_FAST == 1
//       startPwm = startPwm+10;
//     #endif 


//     long DO_NOT_CHECK_BEFORE = 3000 ;
    

//     long START_REDUCING_AT_BALANCE = 1500 ;

//     int applied_break1=0;
//     int applied_break_at1=1000;
//     int applied_break_dur_us1=200;
  

//     int applied_break2=0;
//     int applied_break_at2=800;
//     int applied_break_dur_us2=0;
    
//     int applied_break3=0;
//     int applied_break_at3=0;
//     int applied_break_dur_us3=0;
    

//     if (target_pulse<700){
//       START_REDUCING_AT_BALANCE =1000;
//     }

//     int max_speed=900;
//       //start and stablize
//     setMotor1(max_speed);
//     //setMotor2((startPwm+5)*dir);
//     delay(1500);  
      
//     curr.loop_count=0;
//     UpdateMoveStateEv();

//     while (UpdateMoveStateEv())
//     {
//       curr.loop_count++;;
//       if (curr.avg_remaining>DO_NOT_CHECK_BEFORE){

//         #if DEBUG
//        //LOG_INFO3("EC", headingErr, corr);
//         if (curr.loop_count % 25 ==0){
//            PrintMove();
//         }
//         #endif
//         delay(50);
//         continue;
//       }

//       //  printDebugStatus();
//         int calcPwm= startPwm + overSpeedPwm - underSpeedPwm;
//         // --- Trapezoid profile ---
//         int basePWM =
//             TrapezoidSpeed(calcPwm ,
//                             curr.avg_remaining,
//                             START_REDUCING_AT_BALANCE);


        
//         applyMoveBoost();
//         // --- Heading correction (encoder + gyro) ---
//         float headingErr =
//            0;

//         int corr =0;

//         // --- PWM-only adjustment ---
//        int pwm1 = basePWM + corr +curr.halt.m1_boost;   // stiff wheel
//        int pwm2 = basePWM - corr + curr.halt.m2_boost;          // corrective wheel

//        pwm1 = abs(constrain(pwm1, basePWM - 60 , basePWM + 60));
//        pwm2 = abs(constrain(pwm2, basePWM - 60, basePWM + 60));

//        setMotor1(pwm1*dir);
//       // setMotor2(pwm2*dir);

//       #if DEBUG
//        //LOG_INFO3("EC", headingErr, corr);
//         if (curr.loop_count % 25 ==0){
//            PrintMove();
//         }
//       #endif
      
//       delay(5);
//       StopMotors();
      
//       #if USE_RB_GYRO_FAST == 1
//         delayMicroseconds(200);
//       #else
//          delay(1);
//          delayMicroseconds(200);
//       #endif
      
//       if ( (curr.short_pps.m1+curr.short_pps.m2) >=1300 ){
//           StopMotors();
//           delay(1);
//           overSpeedPwm = overSpeedPwm-10;

//       }
//       else{
//         overSpeedPwm = 0;
//       }
//       if ((curr.short_pps.m1 + curr.short_pps.m2) <=200 && curr.avg_remaining<300   ){
//         //underspeed Pwm
//           underSpeedPwm = underSpeedPwm+10;

//       }
//       else{
//         underSpeedPwm=0;
//       }
//       if (curr.avg_remaining<300){
//         delay(1);
//       }
//       if (curr.avg_remaining<200){
//         delay(1);
//       }
//        if (curr.avg_remaining<100){
//         delay(1);
//       }

//       if (curr.avg_remaining<50){
//         delay(1);
//       }




//     }

//     applyBreak();
//     DEBUG_PRINT("After Break.");
//     PrintMove();

//     delay(50);
//     StopMotors();

//     // settle + debug
//     for (int i = 0; i < 5; i++) {
//         delay(50);
// #if DEBUG
//         //printDebugStatus();
//      //   LOG_INFO3(" PWM 1/2", pwm1, pwm2);
//        DEBUG_PRINT(i);
//        DEBUG_PRINT(".");
       
//       PrintMove();
       

// #endif
//     }
// }
void slowStart(){

  int minSpeed=200;
  int maxSpeed=500;
  int incr =1 ;
  unsigned int wait_ums = 500; // microselc

  for (int i = minSpeed; i <= maxSpeed ; i = i + incr){
       setMotor1(i);
    //setMotor2((startPwm+5)*dir);
    delayMicroseconds(wait_ums); 

  }

}

void moveEvPulseNewLogic(long target_pulse, int dir)
{
    delay(2000);
    Serial.println("moveEvPulse");
    Serial.println(target_pulse);
    PrintMove();

    NextMove(target_pulse,dir);
    PrintMove();
    Serial.println("setup done moveEvPulse");
    Serial.println(target_pulse);

    curr.avg_remaining = target_pulse;

    curr.halt.m1_boost=0;
    curr.halt.m2_boost=0;
    curr.halt.m1_halt_count=0;
    curr.halt.m1_halt_count=0;
    
    

   

    int startPwm = 800;
    int maxPwm=920;
    int normalPwm =400;
    int overSpeedPwm = -1;
    int underSpeedPwm = -1;
    
    #if USE_RB_GYRO_FAST == 1
      startPwm = startPwm+10;
    #endif 

    long tolerance = 150;
    long full_target =  target_pulse;
    long first_target= target_pulse-tolerance;

    long DO_NOT_CHECK_BEFORE = 200 ;

    long stop_step_start_at_balance =2500;
    long stop_step_end_at_balance = 800;
    

    

    long START_REDUCING_AT_BALANCE = 1500 ;

    int applied_break1=0;
    int applied_break_at1=1000;
    int applied_break_dur_us1=200;
  

    int applied_break2=0;
    int applied_break_at2=800;
    int applied_break_dur_us2=0;
    
    int applied_break3=0;
    int applied_break_at3=0;
    int applied_break_dur_us3=0;
    

    if (target_pulse<700){
      START_REDUCING_AT_BALANCE =1000;
    }
    slowStart();

    int max_speed=600;
      //start and stablize
    setMotor1(max_speed);
    //setMotor2((startPwm+5)*dir);
    delay(1000);  
      
    curr.loop_count=0;
    UpdateMoveStateEv();
    PrintMove();
    while (curr.current_pulse.m1 < first_target )
    {
      UpdateMoveStateEv();
      curr.loop_count++;;
      long  bal=  (first_target -curr.current_pulse.m1);
      if ( (first_target -curr.current_pulse.m1) > DO_NOT_CHECK_BEFORE  ){

        #if DEBUG
       //LOG_INFO3("EC", headingErr, corr);
        if (curr.loop_count % 20 ==0){
          Serial.println("Phase 1 Continue");
          Serial.println(curr.loop_count);
          Serial.println((first_target -curr.current_pulse.m1));

          
          PrintMove();
        }
        #endif
        delay(50);
       // #if DEBUG
          //Serial.println("Contine..");
       // #endif
        
        continue;
      }
       
        bal=  (first_target -curr.current_pulse.m1);
       if ( (bal) > stop_step_end_at_balance && curr.short_pps.m1>600 ){
          setMotor1(0); 
       
        #if DEBUG
          
       //LOG_INFO3("EC", headingErr, corr);
        if (curr.loop_count % 25 ==0){
            Serial.println("Phase 2 Continue");

           PrintMove();
        }
        #endif
        delay(1);
        continue;
      }
      




      //  printDebugStatus();
        int calcPwm= normalPwm + overSpeedPwm - underSpeedPwm;
        // --- Trapezoid profile ---
        int basePWM =
            TrapezoidSpeed(calcPwm ,
                            curr.avg_remaining,
                            START_REDUCING_AT_BALANCE);


        
        applyMoveBoost();
        // --- Heading correction (encoder + gyro) ---
        float headingErr =
           0;

        int corr =0;

        // --- PWM-only adjustment ---
       int pwm1 = basePWM + corr +curr.halt.m1_boost;   // stiff wheel
       int pwm2 = basePWM - corr + curr.halt.m2_boost;          // corrective wheel

       pwm1 = abs(constrain(pwm1, basePWM - 60 , basePWM + 60));
       pwm2 = abs(constrain(pwm2, basePWM - 60, basePWM + 60));

       setMotor1(pwm1*dir);
      // setMotor2(pwm2*dir);

      #if DEBUG
       //LOG_INFO3("EC", headingErr, corr);
        if (curr.loop_count % 25 ==0){
           PrintMove();
        }
      #endif
      
      delay(5);
      StopMotors();
      
      #if USE_RB_GYRO_FAST == 1
        delayMicroseconds(200);
      #else
         delay(1);
         delayMicroseconds(200);
      #endif
      
      if ( (curr.short_pps.m1+curr.short_pps.m2) >=1300 ){
          StopMotors();
          delay(1);
          overSpeedPwm = overSpeedPwm-10;

      }
      else{
        overSpeedPwm = 0;
      }
      if ((curr.short_pps.m1 + curr.short_pps.m2) <=200 && curr.avg_remaining<300   ){
        //underspeed Pwm
          underSpeedPwm = underSpeedPwm+10;

      }
      else{
        underSpeedPwm=0;
      }
      if (curr.avg_remaining<300){
        delay(1);
      }
      if (curr.avg_remaining<200){
        delay(1);
      }
       if (curr.avg_remaining<100){
        delay(1);
      }

      if (curr.avg_remaining<50){
        delay(1);
      }




    }

    applyBreak();
    DEBUG_PRINT("After Break.");
    PrintMove();

    delay(50);
    StopMotors();

    // settle + debug
    for (int i = 0; i < 5; i++) {
        delay(50);
#if DEBUG
        //printDebugStatus();
     //   LOG_INFO3(" PWM 1/2", pwm1, pwm2);
       DEBUG_PRINT(i);
       DEBUG_PRINT(".");
       
      PrintMove();
       

#endif
    }
}



void moveEvPulse(long target_pulse, int dir)
{

  return moveEvPulseNewLogic(target_pulse,dir);

    delay(2000);
    Serial.println("moveEvPulse");
    Serial.println(target_pulse);
    PrintMove();

    NextMove(target_pulse,dir);
    PrintMove();
    Serial.println("setup done moveEvPulse");
    Serial.println(target_pulse);

    curr.avg_remaining = target_pulse;

    curr.halt.m1_boost=0;
    curr.halt.m2_boost=0;
    curr.halt.m1_halt_count=0;
    curr.halt.m1_halt_count=0;
    
    

   

    int startPwm = 800;
    int overSpeedPwm = -1;
    int underSpeedPwm = -1;
    
    #if USE_RB_GYRO_FAST == 1
      startPwm = startPwm+10;
    #endif 


    long DO_NOT_CHECK_BEFORE = 3000 ;
    

    long START_REDUCING_AT_BALANCE = 1500 ;

    int applied_break1=0;
    int applied_break_at1=1000;
    int applied_break_dur_us1=200;
  

    int applied_break2=0;
    int applied_break_at2=800;
    int applied_break_dur_us2=0;
    
    int applied_break3=0;
    int applied_break_at3=0;
    int applied_break_dur_us3=0;
    

    if (target_pulse<700){
      START_REDUCING_AT_BALANCE =1000;
    }

    int max_speed=900;
      //start and stablize
    setMotor1(max_speed);
    //setMotor2((startPwm+5)*dir);
    delay(1500);  
      
    curr.loop_count=0;
    UpdateMoveStateEv();

    while (UpdateMoveStateEv())
    {
      curr.loop_count++;;
      if (curr.avg_remaining>DO_NOT_CHECK_BEFORE){

        #if DEBUG
       //LOG_INFO3("EC", headingErr, corr);
        if (curr.loop_count % 25 ==0){
           PrintMove();
        }
        #endif
        delay(50);
        continue;
      }

      //  printDebugStatus();
        int calcPwm= startPwm + overSpeedPwm - underSpeedPwm;
        // --- Trapezoid profile ---
        int basePWM =
            TrapezoidSpeed(calcPwm ,
                            curr.avg_remaining,
                            START_REDUCING_AT_BALANCE);


        
        applyMoveBoost();
        // --- Heading correction (encoder + gyro) ---
        float headingErr =
           0;

        int corr =0;

        // --- PWM-only adjustment ---
       int pwm1 = basePWM + corr +curr.halt.m1_boost;   // stiff wheel
       int pwm2 = basePWM - corr + curr.halt.m2_boost;          // corrective wheel

       pwm1 = abs(constrain(pwm1, basePWM - 60 , basePWM + 60));
       pwm2 = abs(constrain(pwm2, basePWM - 60, basePWM + 60));

       setMotor1(pwm1*dir);
      // setMotor2(pwm2*dir);

      #if DEBUG
       //LOG_INFO3("EC", headingErr, corr);
        if (curr.loop_count % 25 ==0){
           PrintMove();
        }
      #endif
      
      delay(5);
      StopMotors();
      
      #if USE_RB_GYRO_FAST == 1
        delayMicroseconds(200);
      #else
         delay(1);
         delayMicroseconds(200);
      #endif
      
      if ( (curr.short_pps.m1+curr.short_pps.m2) >=1300 ){
          StopMotors();
          delay(1);
          overSpeedPwm = overSpeedPwm-10;

      }
      else{
        overSpeedPwm = 0;
      }
      if ((curr.short_pps.m1 + curr.short_pps.m2) <=200 && curr.avg_remaining<300   ){
        //underspeed Pwm
          underSpeedPwm = underSpeedPwm+10;

      }
      else{
        underSpeedPwm=0;
      }
      if (curr.avg_remaining<300){
        delay(1);
      }
      if (curr.avg_remaining<200){
        delay(1);
      }
       if (curr.avg_remaining<100){
        delay(1);
      }

      if (curr.avg_remaining<50){
        delay(1);
      }




    }

    applyBreak();
    DEBUG_PRINT("After Break.");
    PrintMove();

    delay(50);
    StopMotors();

    // settle + debug
    for (int i = 0; i < 5; i++) {
        delay(50);
#if DEBUG
        //printDebugStatus();
     //   LOG_INFO3(" PWM 1/2", pwm1, pwm2);
       DEBUG_PRINT(i);
       DEBUG_PRINT(".");
       
      PrintMove();
       

#endif
    }
  
}



