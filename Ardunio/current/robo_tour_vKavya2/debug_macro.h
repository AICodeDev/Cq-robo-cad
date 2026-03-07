#pragma once
#include <Arduino.h>
#include "SafeLogger.h"
extern SafeBleLogger bleLogger;


#define DEBUG 0
#define DEBUG_BLE 0

// --- CONFIGURATION ---
#define LOG_LEVEL 4          // 0:OFF, 1:ERR, 2:WRN, 3:INF, 4:DBG, 5:TRC
#define MODE_SAFE_BLE    // Choose: MODE_NORMAL_SERIAL, MODE_SAFE_BLE, MODE_NO_LOG

#if DEBUG_BLE
  #define BLE_LOG(x) {bleLogger.print(x);}

#else
  #define BLE_LOG(x)

#endif

#if DEBUG_BLE
  // Use __VA_ARGS__ to pass all arguments to the logger's printf method
  #define BLE_LOGF(...) bleLogger.printf(__VA_ARGS__)
#else
  // Compiles to nothing when DEBUG_BLE is false
  #define BLE_LOGF(...) 
#endif


// --- OUTPUT ROUTING ENGINE ---
#if defined(MODE_NO_LOG)
  #define ANY_LOG(lvl, p1, p2, p3, p4, p5)
  #define LINE_LOG(p1)
  
#elif defined(MODE_SAFE_BLE)
  //#define ANY_LOG(lvl, p1, p2, p3, p4, p5) { bleLogger.print(lvl);   bleLogger.print(String(p1));  bleLogger.print(String(p2));  bleLogger.print(String(p3)); ;  bleLogger.print(String(p4));  bleLogger.print(String(p5)); } 

    #define ANY_LOG(lvl, p1, p2, p3, p4, p5) { \
    String msg = "-" ; \
    msg += String(p1); \
    msg += String(" "); \    
    msg += String(p2); \
    msg += String(" "); \
    msg += String(p3); \
    msg += String(" "); \
    msg += String(p4); \
    msg += String(" "); \
    msg += String(p5); \
    bleLogger.print(msg);    }

    

  #define LINE_LOG(p1) { bleLogger.print(String(p1)); Serial.println("");  }
#else
  #define ANY_LOG(lvl, p1, p2, p3, p4, p5) { Serial.print(lvl);  Serial.print(p1); Serial.print(p2); Serial.print(p3);     Serial.print(p4); Serial.println(p5); }
  #define LINE_LOG(p1) {Serial.println(p1); }

#endif

// --- ERROR (Level 1) ---
      #if LOG_LEVEL >= 1
        #define LOG_ERROR3(p1, p2, p3)         ANY_LOG("ERR", p1, p2, p3, "", "")
        #define LOG_ERROR4(p1, p2, p3, p4)     ANY_LOG("ERR", p1, p2, p3, p4, "")
        #define LOG_ERROR5(p1, p2, p3, p4, p5) ANY_LOG("ERR", p1, p2, p3, p4, p5)
      #else
        #define LOG_ERROR3(p1, p2, p3)
        #define LOG_ERROR4(p1, p2, p3, p4)
        #define LOG_ERROR5(p1, p2, p3, p4, p5)
      #endif

// --- INFO (Level 3) ---
    // #if LOG_LEVEL >= 3
    //   #define LOG_INFO3(p1, p2, p3)          ANY_LOG("INF", p1, p2, p3, "", "")
    //   #define LOG_INFO4(p1, p2, p3, p4)      ANY_LOG("INF", p1, p2, p3, p4, "")
    //   #define LOG_INFO5(p1, p2, p3, p4, p5)  ANY_LOG("INF", p1, p2, p3, p4, p5)
    // #else
    //   #define LOG_INFO3(p1, p2, p3)
    //   #define LOG_INFO4(p1, p2, p3, p4)
    //   #define LOG_INFO5(p1, p2, p3, p4, p5)
    // #endif

// --- DEBUG (Level 4) ---
      // #if LOG_LEVEL >= 4
      //   #define LOG_DEBUG3(p1, p2, p3)         ANY_LOG("DBG", p1, p2, p3, "", "")
      //   #define LOG_DEBUG4(p1, p2, p3, p4)     ANY_LOG("DBG", p1, p2, p3, p4, "")
      //   #define LOG_DEBUG5(p1, p2, p3, p4, p5) ANY_LOG("DBG", p1, p2, p3, p4, p5)
      // #else
      //   #define LOG_DEBUG3(p1, p2, p3)
      //   #define LOG_DEBUG4(p1, p2, p3, p4)
      //   #define LOG_DEBUG5(p1, p2, p3, p4, p5)
      // #endif

// --- TRACE (Level 5) ---
      #if LOG_LEVEL >= 5
        #define LOG_TRACE3(p1, p2, p3)         ANY_LOG("TRC", p1, p2, p3, "", "")
        #define LOG_TRACE4(p1, p2, p3, p4)     ANY_LOG("TRC", p1, p2, p3, p4, "")
        #define LOG_TRACE5(p1, p2, p3, p4, p5) ANY_LOG("TRC", p1, p2, p3, p4, p5)
      #else
        #define LOG_TRACE3(p1, p2, p3)
        #define LOG_TRACE4(p1, p2, p3, p4)
        #define LOG_TRACE5(p1, p2, p3, p4, p5)
      #endif











// ERROR (1)
#if LOG_LEVEL >= 1
  #define LOG_ERROR1(p1) ANY_LOG("ERR", p1, "","","","")
  #define LOG_ERROR2(p1,p2) ANY_LOG("ERR", p1, p2,"","","")
  #define LOG_ERROR3(p1,p2,p3) ANY_LOG("ERR", p1, p2, p3,"","")
  #define LOG_ERRORLN(p1) ANY_LOG("ERR", p1, "","","","")
#else
  #define LOG_ERROR1(p1) 
  #define LOG_ERROR2(p1,p2)
  #define LOG_ERROR3(p1,p2,p3)
  #define LOG_ERRORLN(p1)
#endif

// INFO (3)
#if LOG_LEVEL >= 3
  #define LOG_INFO1(p1) ANY_LOG("INF", p1, "\n","","","")
  #define LOG_XINFO2(p1,p2) ANY_LOG("INF", p1, p2,"\n","","")
  #define LOG_INFO3(p1,p2,p3) ANY_LOG("I ", p1, p2, p3,"\n","")
  #define LOG_INFO4(p1,p2,p3,p4) ANY_LOG("INF", p1, p2, p3, p4, "\n")
  #define LOG_INFO5(p1,p2,p3,p4,p5) ANY_LOG("INF", p1, p2, p3, p4, p5)
  #define LOG_INFOLN(p1)  LINE_LOG(p1)
#else
  #define LOG_INFO1(p1)
  #define LOG_INFO2(p1,p2)
  #define LOG_INFO3(p1,p2,p3)
  #define LOG_INFO4(p1,p2,p3,p4)
  #define LOG_INFO5(p1,p2,p3,p4,p5)
  #define LOG_INFOLN(p1)
#endif

// DEBUG (4)
#if LOG_LEVEL >= 4
  #define LOG_DEBUG1(p1) ANY_LOG("DBG", p1, "","","","")
  #define LOG_DEBUG2(p1,p2) ANY_LOG("DBG", p1, p2,"","","")
  #define LOG_DEBUG3(p1, p2, p3)         ANY_LOG("DBG", p1, p2, p3, "", "")
  #define LOG_DEBUG4(p1, p2, p3, p4)     ANY_LOG("DBG", p1, p2, p3, p4, "")

  #define LOG_DEBUG5(p1,p2,p3,p4,p5) ANY_LOG("DBG", p1, p2, p3, p4, p5)
  #define LOG_DEBUGLN(p1) LINE_LOG(p1)
#else
  #define LOG_DEBUG1(p1)
  #define LOG_DEBUG2(p1,p2)
  #define LOG_DEBUG3(p1, p2, p3)
  #define LOG_DEBUG4(p1, p2, p3, p4)
        
  #define LOG_DEBUG5(p1,p2,p3,p4,p5)
  #define LOG_DEBUGLN(p1)
#endif






