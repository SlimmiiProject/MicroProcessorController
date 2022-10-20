#ifndef Http_h
#define Http_h 
#include "Arduino.h"
#include <WiFi.h>

class Http
{
  public: 
    void init(uint16_t port);
    void handleClient(bool waitForConnect);

};
#endif
