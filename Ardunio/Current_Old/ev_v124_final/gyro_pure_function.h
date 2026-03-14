#pragma once

inline void fullStop(){
   digitalWrite(20, LOW);
}

inline void restart(){
   digitalWrite(20, HIGH);
}


// Add angle normalization function
inline float normalizeAngle2(float angle) {
  while (angle > 180.0) angle -= 360.0;
  while (angle < -180.0) angle += 360.0;
  return angle;
}


int TrapezoidSpeedForGyro(int base_pwm, float remaining_degrees, float start_reducing_at) {
    float abs_remaining = abs(remaining_degrees);
    
    // Full speed zone - far from target
    if (abs_remaining >= start_reducing_at) {
        return base_pwm;
    }
    
    // Deceleration zone - linear reduction
    // From base_pwm down to MIN_PWM_TURN_M1
    int speed_range = base_pwm - 100;
    int scaled_pwm = 150 + (int)((speed_range * abs_remaining) / start_reducing_at);
    
    return constrain(scaled_pwm, 100, base_pwm);
}
