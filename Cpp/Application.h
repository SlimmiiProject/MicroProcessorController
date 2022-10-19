#ifndef Application_h
#define Application_h 
#include "Arduino.h"
#include "Network.h"
#include <SPIFFS.h>

class Application 
{
  public: 
    /** @description: Setup the enviroment and application services */
    void setup(); 

    /** @description: The main execution loop for the application. */
    void main(); 
  
  private: 
    Network net; 
};

#endif 