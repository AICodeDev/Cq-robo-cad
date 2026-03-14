// #pragam once

// //#include <RoboBloqDrive.h>
// /*
// #include "RB_BUZZER.h"


// #define USER_KEY_Pin 35
// #define BUZZER_Pin 36  // Change to your buzzer pin


// RB_Buzzer buzzer(BUZZER_Pin);
// */


// // void setup() {
// //   Serial.begin(9600);
// //   pinMode(USER_KEY_Pin, INPUT);
// //   Serial.println("Press button: Each = 0.25m");
// // }

// void checkButtonCount() {

//   while (1)
//   {

//     Button_Process();
  
//   // After 2 seconds of no press, enter wait_for_start mode
//     if (!wait_for_start && button_count > 0) {
//       if (millis() - last_press_time >= 5000) {
//         wait_for_start = true;
//         target_distance = button_count * 0.1;
        
//         // Beep 500ms when entering wait_for_start
//         buzzer.tone(800, 900);
        
//         Serial.print("Distance set: ");
//         Serial.print(target_distance);
//         Serial.println("m. Press button to START");
//       }
//     }
  
//   // In wait_for_start mode, if button pressed, wait 1 sec then start
//     if (wait_for_start && start_press_time > 0) {
//       if (millis() - start_press_time >= 1000) {
        
//         // Beep 1 second when motor starts
//         buzzer.tone(1000, 1000);
//         MainRun();
        
//         Serial.println("MOTOR STARTED!");
        
//         // Reset
//         button_count = 0;
//         wait_for_start = false;
//         start_press_time = 0;
//       }
//     }
//   }

// }

// void Button_Process() {
//   if (digitalRead(USER_KEY_Pin) == HIGH) {
//     Hardware_Button_flag = true;
//   }
  
//   if (digitalRead(USER_KEY_Pin) == LOW && Hardware_Button_flag) {
//     Button_Down = true;
//     Hardware_Button_flag = false;
//   }
  
//   if (Button_Down) {
//     Button_Down = false;
    
//     if (!wait_for_start) {
//       // Count distance
//       button_count++;
//       last_press_time = millis();
      
//       // Beep 50ms if count is divisible by 5
//       if (button_count % 10 == 0) {
//          Serial.print("button_count % 5 == 0");
//         Serial.println("small beep");
//         buzzer.tone(1500, 100);

//       }
      
//       Serial.print("Count: ");
//       Serial.print(button_count);
//       Serial.print(" = ");
//       Serial.print(button_count * 0.1);
//       Serial.println("m");
//     } else {
//       // Start button pressed
//       start_press_time = millis();
//       Serial.println("Starting in 1 second...");
//     }
//   }
// }



// /*#define USER_KEY_Pin 35

// bool Hardware_Button_flag = false;
// bool Button_Down = false;
// int button_count = 0;
// bool wait_for_start = false;
// unsigned long last_press_time = 0;
// unsigned long start_press_time = 0;
// float target_distance = 0;

// void setup() {
//   Serial.begin(9600);
//   pinMode(USER_KEY_Pin, INPUT);
//   Serial.println("Press button: Each = 0.1m");
// }

// void loop() {
//   Button_Process();
  
//   // After 2 seconds of no press, enter wait_for_start mode
//   if (!wait_for_start && button_count > 0) {
//     if (millis() - last_press_time >= 2000) {
//       wait_for_start = true;
//       target_distance = button_count * 0.1;
//       Serial.print("Distance set: ");
//       Serial.print(target_distance);
//       Serial.println("m. Press button to START");
//     }
//   }
  
//   // In wait_for_start mode, if button pressed, wait 1 sec then start
//   if (wait_for_start && start_press_time > 0) {
//     if (millis() - start_press_time >= 1000) {
//       Serial.println("MOTOR STARTED!");
      
//       // Reset
//       button_count = 0;
//       wait_for_start = false;
//       start_press_time = 0;
//     }
//   }
// }

// void Button_Process() {
//   if (digitalRead(USER_KEY_Pin) == HIGH) {
//     Hardware_Button_flag = true;
//   }
  
//   if (digitalRead(USER_KEY_Pin) == LOW && Hardware_Button_flag) {
//     Button_Down = true;
//     Hardware_Button_flag = false;
//   }
  
//   if (Button_Down) {
//     Button_Down = false;
    
//     if (!wait_for_start) {
//       // Count distance
//       button_count++;
//       last_press_time = millis();
//       Serial.print("Count: ");
//       Serial.print(button_count);
//       Serial.print(" = ");
//       Serial.print(button_count * 0.1);
//       Serial.println("m");
//     } else {
//       // Start button pressed
//       start_press_time = millis();
//       Serial.println("Starting in 1 second...");
//     }
//   }
// }*/