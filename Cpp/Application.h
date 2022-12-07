#ifndef Application_h
#define Application_h 
#include <SPIFFS.h>
#include "Arduino.h"
#include "Network.h"
#include "Http.h"
#include "API.h"

#define DEBUG 1
#define DELAY_MS_LOOP 1000
#define TICK_IN_MS 1000
#define TICKS_REQUIRED 10


class Application 
{
  private: 
    /** @description: Check or the first device initialization has been done, perform if needed */
    static void initDefaults();
    /** @description: Initialize the device hardware functionality */
    static void initHardware();

  public: 
    /** @description: Setup the enviroment and application services */
    static void setup(); 

    /** @description: The main execution loop for the application. */
    static void main(); 
};

#endif 