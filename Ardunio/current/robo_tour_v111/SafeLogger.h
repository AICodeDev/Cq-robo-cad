#pragma once

#include <Arduino.h>


const char* formatToStaticBuffer(const char* format, ...) {
    static char buffer[128]; // Adjust size based on your 'maxBytes'
    va_list args;
    va_start(args, format);
    vsnprintf(buffer, sizeof(buffer), format, args);
    va_end(args);
    return buffer;
}


class SafeBleLogger {
private:
    unsigned long lastWriteTime = 0;
    const unsigned long interval = 50; // 100ms
    const int maxBytes = 100;

public:
  void printf(const char* format, ...) {
     static char buffer[128];
        va_list args;
        va_start(args, format);
        
        // Use vsnprintf for variable arguments with a va_list
        vsnprintf(buffer, sizeof(buffer), format, args);
        
        va_end(args);

        // Pass the formatted buffer to your print logic
        print(buffer);
    }

   void print(const char* msg) {
    if (millis() - lastWriteTime >= interval) {
        int len = strlen(msg);
        if (len > maxBytes) len = maxBytes; 

        if (Serial.availableForWrite() >= len) {
            Serial.write((const uint8_t*)msg, len);
            Serial.println(); 
            lastWriteTime = millis();
        }
    }
}


 void print(const String& msg) {
    if (millis() - lastWriteTime >= interval) {
        int len = msg.length();
        if (len > maxBytes) len = maxBytes; // Truncate to 20 bytes (e.g., 20)

        // Only write if the Serial hardware buffer has enough room
        if (Serial.availableForWrite() >= len) {
            // Write only up to 'len' bytes from the String
            Serial.write(msg.c_str(), len);
            Serial.println(); // Line break
            lastWriteTime = millis();
        }
    }
    // If timing or buffer isn't ready, data is simply ignored
}

    // Overload for numbers if needed
    void print(int val) {
        char buf[10];
        itoa(val, buf, 10);
        print(buf);
    }
};

SafeBleLogger bleLogger;

