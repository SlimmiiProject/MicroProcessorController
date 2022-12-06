#ifndef Application_h
#define Application_h 
#include <SPIFFS.h>
#include "Arduino.h"
#include "Network.h"
#include "Http.h"
#include "API.h"

class Application 
{
  public: 
    /** @description: Setup the enviroment and application services */
    static void setup(); 

    /** @description: The main execution loop for the application. */
    static void main(); 
};

#endif 