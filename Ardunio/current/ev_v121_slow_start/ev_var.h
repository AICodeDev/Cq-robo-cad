#pragma once

#include "RB_ENCONDERMOTOR.h"
#include "RB_BUZZER.h"


//volatile long encoder_count = 0;

float how_much_it_should_go =3000;
float how_much_it_is_going =3000;//3401
float caliber_factor = how_much_it_should_go/how_much_it_is_going;
float PULSES_PER_MM_EV = (2.4* caliber_factor)  ;

const float BASE_DISTANCE = 2000.0;  // Starting distance in mm
const float DISTANCE_INCREMENT = 250.0;  // mm per button press
const unsigned long DOUBLE_CLICK_TIME = 300;  // ms for double-click detection
const unsigned long START_TIMEOUT = 3000;  // ms before auto-start
int ev_done=0;
