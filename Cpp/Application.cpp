#include "Application.h"
#include "Arduino.h"
#include <SPIFFS.h>
#include "Network.h"
#include "Http.h"


void Application::setup()
{
  Serial.begin(115200);  // Setup serial connection based on device upload speed.
  SPIFFS.begin(true);    // Setup IO

  // Setup enviroment variables
  setenv("CONFIG_PATH",     "/conf/", 0);
  setenv("AP_PROFILE_PATH", (String(getenv("CONFIG_PATH"))+String("ap.bin")).c_str(), 0);
  setenv("WIFI_PROFILE_PATH", (String(getenv("CONFIG_PATH"))+String("wifi.bin")).c_str(), 0);

  net.createAccessPoint("SlimiMeter", "H3LL0FR0MSL1M1IMaTesTAnDWILLB3ChanG3d");
  net.wifiConnect("", "");

  http.init(80);
}

void Application::main()
{
  IPAddress wip = net.wifiIP();
  if(wip.toString() != "0.0.0.0")
    Serial.printf("IP Address = %s", wip.toString()+"\n");
  else 
    Serial.println("No wifi connection");

  IPAddress aip = net.apIP();
  if(aip.toString() != "0.0.0.0")
    Serial.printf("Access point IP Address = %s", aip.toString()+"\n");
  else 
    Serial.println("No wifi connection");
  
  http.handleClient(true);
  delay(1000);
}