inline float deg2rad(float d) { return d * 0.0174532925f; }
inline float rad2deg(float r) { return r * 57.2957795f; }

inline float NormalizeAngle(float a)
{
    while (a > PI)  a -= TWO_PI;
    while (a < -PI) a += TWO_PI;
    return a;
}

float normalizeRBAngle(float angle) {
    // 1. Use modulo to get the remainder within [-360, 360]
    angle = fmod(angle, 360.0f);

    // 2. If the result is > 180, subtract 360 to get the negative equivalent
    if (angle > 180.0f) {
        angle -= 360.0f;
    }
    // 3. If the result is <= -180, add 360 to get the positive equivalent
    else if (angle <= -180.0f) {
        angle += 360.0f;
    }

    return angle;
}


inline int TrapezoidSpeed(int base, long remaining, long startReduce)
{
    if (remaining >= startReduce) return base;

    float scale = (float)remaining / (float)startReduce;
    if (scale < 0.30f) scale = 0.30f;   // don’t stall

    return (int)(base * scale);
}

inline int HeadingPWMCorrection(float headingDeg)
{
    const float KP = 2.5f;   // tune this
    int corr = (int)(KP * headingDeg);
    return constrain(corr, -40, 40);
}

// Constraints (Adjust these for your robot)
const float MAX_VEL = 400.0;  // pulses per second
const float ACCEL   = 200.0;  // pulses per second^2

long CalculateTrapezoidSetpoint(unsigned long elapsedMs, long totalDistance) {
    float t = elapsedMs / 1000.0; // convert to seconds
    
    // 1. Calculate critical time points
    float t_acc = MAX_VEL / ACCEL;
    float dist_acc = 0.5 * ACCEL * t_acc * t_acc;
    
    // Handle short moves where we never reach MAX_VEL (Triangular profile)
    if (dist_acc * 2 > totalDistance) {
        t_acc = sqrt(totalDistance / ACCEL);
        dist_acc = 0.5 * ACCEL * t_acc * t_acc;
    }
    
    float dist_const = totalDistance - (2 * dist_acc);
    float t_const = dist_const / MAX_VEL;
    float t_dec_start = t_acc + t_const;
    float t_total = t_dec_start + t_acc;

    // 2. Calculate setpoint based on current phase
    if (t < t_acc) {
        // Phase 1: Acceleration
        return (long)(0.5 * ACCEL * t * t);
    } 
    else if (t < t_dec_start) {
        // Phase 2: Constant Velocity
        float time_in_const = t - t_acc;
        return (long)(dist_acc + (MAX_VEL * time_in_const));
    } 
    else if (t < t_total) {
        // Phase 3: Deceleration
        float time_in_dec = t - t_dec_start;
        float v_at_dec_start = MAX_VEL; 
        return (long)(dist_acc + dist_const + (v_at_dec_start * time_in_dec) - (0.5 * ACCEL * time_in_dec * time_in_dec));
    } 
    else {
        // Finished
        return totalDistance;
    }
}

/**
 * Calculate completion percentage based on average of both motors
 */
float getCompletionPercent(long m1_count1, long m2_count1, long target_pulses) {
  long avg_count = (m1_count1 + m2_count1) / 2;
  float percent = ((float)avg_count / (float)target_pulses) * 100.0;
  return constrain(percent, 0.0, 100.0);
}