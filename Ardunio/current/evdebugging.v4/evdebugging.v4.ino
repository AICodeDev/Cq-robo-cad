#include "RB_ENCONDERMOTOR.h"
#include "RB_BUZZER.h"

RB_EncoderMotor M1(1);
RB_EncoderMotor M2(2);
volatile long encoder_count = 0;

const float PULSES_PER_MM = (3)  ;

//#include <RoboBloqDrive.h>

//What distance you want to go?  6.25 -- Dynamic
//What is base distance/mini disance // 5 //Pre configured
//What is the increment for each button. 25 CM  //Pre configured 
//How much time you need to press the button? 


#define USER_KEY_Pin 35 
#define BUZZER_Pin 36  // Change to your buzzer pin

#define RGB_LED_Pin    37


//RB_Buzzer buzzer(BUZZER_Pin);


// Button configuration
const int BUTTON_PIN = USER_KEY_Pin;
const int BUZZER_PIN = BUZZER_Pin;  // Change to your buzzer pin
const float BASE_DISTANCE = 2500.0;  // Starting distance in mm
const float DISTANCE_INCREMENT = 250.0;  // mm per button press
const unsigned long DOUBLE_CLICK_TIME = 300;  // ms for double-click detection
const unsigned long START_TIMEOUT = 3000;  // ms before auto-start

class DistanceSelector {
private:
  int press_count;
  unsigned long last_press_time;
  unsigned long first_press_time;
  bool button_was_pressed;
  bool ready_to_start;
  
public:
  DistanceSelector() {
    press_count = 0;
    last_press_time = 0;
    first_press_time = 0;
    button_was_pressed = false;
    ready_to_start = false;
  }
  
  void begin() {
    pinMode(BUTTON_PIN, INPUT_PULLUP);
    pinMode(BUZZER_PIN, OUTPUT);
  }
  
  float getTargetDistance() {
    return BASE_DISTANCE + (press_count * DISTANCE_INCREMENT);
  }
  
  bool isReadyToStart() {
    return ready_to_start;
  }
  
  void resetReady() {
    ready_to_start = false;
  }
  
  void update() {
    bool button_pressed = (digitalRead(BUTTON_PIN) == LOW);
    unsigned long now = millis();
    
    // Detect button press (edge detection)
    if (button_pressed && !button_was_pressed) {
      // Button just pressed
      
      // Check for double-click (reset)
      if (now - last_press_time < DOUBLE_CLICK_TIME) {
        // Double-click detected - RESET
        press_count = 0;
        resetBeep();  // Special reset beep
        blinkFeedback(3);  // 3 fast blinks = reset
      } else {
        // Single press - increment
        press_count++;
        first_press_time = (press_count == 1) ? now : first_press_time;
        clickBeep();  // Normal click beep
        blinkFeedback(1);  // 1 blink = increment
      }
      
      last_press_time = now;
    }
    
    button_was_pressed = button_pressed;
    
    // Check if 3 seconds passed without button press - START!
    if (press_count > 0 && !ready_to_start) {
      if (now - last_press_time >= START_TIMEOUT) {
        ready_to_start = true;
        blinkFeedback(5);  // 5 blinks = starting!
      }
    }
  }
  
private:
  void clickBeep() {
    // Short single beep for normal press
    tone(BUZZER_PIN, 2000, 100);  // 2kHz for 100ms
  }
  
  void resetBeep() {
    // Two-tone beep for reset
    tone(BUZZER_PIN, 1500, 80);
    delay(100);
    tone(BUZZER_PIN, 1000, 80);
    delay(100);
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

DistanceSelector selector;

void setup() {
  Serial.begin(9600);
  pinMode(20, OUTPUT);
  digitalWrite(20, HIGH);
  
  M1.SetMotionMode(PWM_MODE);
  M2.SetMotionMode(PWM_MODE);
  attachInterrupt(M1.GetIntterrruptNum(), encoderISR, CHANGE);
  
  selector.begin();
  
  
}

void loop() {
  selector.update();
  
  if (selector.isReadyToStart()) {
    float target = selector.getTargetDistance();
    

    
    goStraight(target);
    M1.SetMotorPwm(0);
    

    
    selector.resetReady();
    delay(20000);  // Pause before accepting new input
  }
  
  delay(10);
}

void goStraight(float mm) {
  long target = mm * PULSES_PER_MM;
  long stop = target * 0.98;
  long start = encoder_count;
  
  M1.SetMotorPwm(50);
  
  while (encoder_count - start < stop) {
    long p = encoder_count - start;
    if (p >= stop) break;
    
    if (p >= target * 0.95) {
      M1.SetMotorPwm(0);
      if (encoder_count - start >= stop) break;
      M1.SetMotorPwm(20);
      delay(1);
      M1.SetMotorPwm(0);
      delay(50);
    }
    else if (p >= target * 0.90) { M1.SetMotorPwm(22); delay(200); }
    else if (p >= target * 0.85) { M1.SetMotorPwm(0); delay(100); M1.SetMotorPwm(25); }
    else if (p >= target * 0.80) { M1.SetMotorPwm(0); delay(100); M1.SetMotorPwm(28); }
    else if (p >= target * 0.75) { M1.SetMotorPwm(0); delay(100); M1.SetMotorPwm(32); }
    else if (p >= target * 0.70) { M1.SetMotorPwm(0); delay(100); M1.SetMotorPwm(35); }
    
    delay(10);
  }
  M1.SetMotorPwm(0);
}

void encoderISR() {
  encoder_count++;
}