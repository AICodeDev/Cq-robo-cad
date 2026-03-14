#pragma once

#define BIG_WHEEL 1 


#ifdef BIG_WHEEL

    #define FACTOR1 1.0
    #define TICK_PER_CM1 50

    #define PULSE_PER_MM 1.98
    #define PULSE_PER_CM 19.8
    


#else

  #define FACTOR1 1.0
  #define TICK_PER_CM1 50
  #define PULSE_PER_MM 1.975
  #define PULSE_PER_CM 19.75
    

#endif

// const float V_TICK_PER_CM = 1 ;
// const float V_FACTOR  = 1.0 ;

