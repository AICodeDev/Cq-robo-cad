#ifndef RB_GYRO_FAST_H
#define RB_GYRO_FAST_H

#include "RB_GYRO.h"
#include <math.h>
#include <util/delay.h>
#include <string.h>
#include "avr/wdt.h"
/**
 * @class RB_GYRO_FAST
 * @brief Optimized for Software I2C to prevent motor lag and handle 90-degree turns.
 */// MPU 9050
class RB_GYRO_FAST : public RB_GYRO {
public:
    unsigned long last_update_ms;
    float start_reference_z;

public:
    uint8_t min_delay_ms; // Minimum time between I2C reads to save CPU
    float GlobalAngleZ;
    float LocalAngleZ;
    float gyroZ;
    float gyroZoffset;
    uint8_t i2cLocalData [14];
     float gSensitivity1;
    float getGlobalZ(){
      return GlobalAngleZ;
    }
    setRefreshRate(int ms){
      min_delay_ms = ms; 
    }
    fastRefresh(){
       min_delay_ms = 15; 
    }

    slowRefresh(){
       min_delay_ms = 50; 
    }

    // Constructor: Defaults to 10ms safety delay
    RB_GYRO_FAST(uint8_t port = 0) : RB_GYRO(port) {
        min_delay_ms = 35; 
        last_update_ms = 0;
        GlobalAngleZ = 0;
        LocalAngleZ = 0;
        start_reference_z = 0;
        gSensitivity1=0;
    }

    inline void start(void) {
        GlobalAngleZ = 0;
        LocalAngleZ =  0;
        min_delay_ms = 35; 
        last_update_ms = 0;
        GlobalAngleZ = 0;
        LocalAngleZ = 0;
        start_reference_z = 0;
        gSensitivity1 = 65.5 ;

        gyroZoffset = 0;

	
      delay(100);
      WriteReg(0x6B,0X00);
      delay(30);
      WriteReg(0X1A,0X01);
      WriteReg(0X1B,0X08);
      delay(50);
      
        calibrateZ(100);

    
    }

    /**
     * @brief Resets the local turn counter to 0.0 based on current heading.
     */
    inline void resetLocal(void) {
        start_reference_z = GlobalAngleZ;
        LocalAngleZ = 0;
    }

    /**
     * @brief Smart update function. 
     * If called faster than min_delay_ms, it returns immediately to save CPU.
     * Otherwise, performs a fast 2-byte Z-axis read.
     * @return Current LocalAngleZ (degrees since last reset)
     */
    inline float updateZ(void) {
        unsigned long now = millis();
        
        // 1. Guard Clause: Skip I2C if called too soon
        if ((now - last_update_ms) < min_delay_ms) {
            return LocalAngleZ; 
        }

        // 2. Timing calculation
        float dt = (float)(now - last_update_ms) * 0.001;
        last_update_ms = now;

        // 3. Fast I2C Read: Only 2 bytes (Gyro Z)
        // 0x47 = Gyro Z High Byte
        ReadData(0x47, i2cLocalData, 2); 
        
        int16_t rawZ = (int16_t)((i2cLocalData[0] << 8) | i2cLocalData[1]);
        
        // 4. Update Velocity (degrees per second)
        gyroZ = (float)(rawZ - gyroZoffset) / gSensitivity1;
        
        // 5. Integrate for Global Heading
        GlobalAngleZ += gyroZ * dt;

        // Wrap Global Heading (-180 to 180)
        if (GlobalAngleZ > 180.0)  GlobalAngleZ -= 360.0;
        else if (GlobalAngleZ < -180.0) GlobalAngleZ += 360.0;

        // 6. Calculate Local Heading (relative to reset point)
        LocalAngleZ = GlobalAngleZ - start_reference_z;
        
        // Handle wrapping for the local turn
        if (LocalAngleZ > 180.0)  LocalAngleZ -= 360.0;
        else if (LocalAngleZ < -180.0) LocalAngleZ += 360.0;

        return LocalAngleZ;
    }

    /**
     * @brief High-precision calibration for Z-axis drift.
     * Call this in setup() while the robot is perfectly still.
     */
    inline void calibrateZ(uint16_t samples = 300) {
        long zsum = 0;
        for(uint16_t i = 0; i < samples; i++) {
            ReadData(0x47, i2cLocalData, 2);
            zsum += (int16_t)((i2cLocalData[0] << 8) | i2cLocalData[1]);
            _delay_ms(2);
            wdt_reset();
        }
        gyroZoffset = (float)zsum / (float)samples;
       // Serial.println(gyroZoffset);
    }
};

#endif
