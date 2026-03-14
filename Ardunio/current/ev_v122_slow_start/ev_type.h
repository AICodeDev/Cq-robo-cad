#pragma once


#include "RB_ENCONDERMOTOR.h"
#include "RB_BUZZER.h"
#include "RB_Port.h"
#include "ev_var.h"



class DistanceSelector {
private:
  int btn_press_count;
  unsigned long last_press_time;
  unsigned long first_press_time;
  bool button_was_pressed;
  bool ready_to_start;
  
public:
  DistanceSelector() {
    btn_press_count = 0;
    last_press_time = 0;
    first_press_time = 0;
    button_was_pressed = false;
    ready_to_start = false;
  }
  
  void begin() {
    pinMode(USER_KEY_Pin, INPUT_PULLUP);
    pinMode(Buzzer_Pin, OUTPUT);
  }
  
  float getTargetDistance() {
    return BASE_DISTANCE + (btn_press_count * DISTANCE_INCREMENT);
  }
  
  bool isReadyToStart() {
    return ready_to_start;
  }
  
  void resetReady() {
    ready_to_start = false;
  }
  
  void update() {
    bool button_pressed = (digitalRead(USER_KEY_Pin) == LOW);
    unsigned long now = millis();
    
    // Detect button press (edge detection)
    if (button_pressed && !button_was_pressed) {
      // Button just pressed
      
      // Check for double-click (reset)
      if (now - last_press_time < DOUBLE_CLICK_TIME) {
        // Double-click detected - RESET
        btn_press_count = 0;
        resetBeep();  // Special reset beep
        blinkFeedback(3);  // 3 fast blinks = reset
      } else {
        
        btn_press_count++;
        //todo fix code merge issue
      
      }
      
      last_press_time = now;
    }
    
    button_was_pressed = button_pressed;
    
    // Check if 3 seconds passed without button press - START!
    if (btn_press_count > 0 && !ready_to_start) {
      if (now - last_press_time >= START_TIMEOUT) {
        ready_to_start = true;
        blinkFeedback(5);  // 5 blinks = starting!
      }
    }
  }
  
private:
  void clickBeep() {
    // Short single beep for normal press
    tone(Buzzer_Pin, 2000, 100);  // 2kHz for 100ms
  }
  
  void resetBeep() {
    // Two-tone beep for reset
    tone(Buzzer_Pin, 1500, 80);
    delay(50);
    tone(Buzzer_Pin, 1000, 80);
    delay(50);
  }
  
  void blinkFeedback(int count) {
    for (int i = 0; i < count; i++) {
      digitalWrite(20, LOW);
      delay(50);
      digitalWrite(20, HIGH);
      delay(50);
    }
  }
};


