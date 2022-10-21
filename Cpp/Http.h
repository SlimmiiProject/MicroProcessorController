#ifndef Http_h
#define Http_h 
#include "Arduino.h"
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <WiFi.h>
#include "Camera.h"

/***
* Http server with master page implementation. 
*/
class Http
{
  public: 
    void init();
  
  private:
    Camera camera; 
    static void getPage(AsyncWebServerRequest *request);
    static char* getPageState();
    static String templateParser(const String& key);
};
#endif
