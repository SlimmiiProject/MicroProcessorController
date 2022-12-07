#include <SPIFFS.h>
#include "Arduino.h"

#include "Application.h"
#include "Network.h"
#include "Http.h"
#include "Camera.h"
#include "API.h"
#include "Device.h"
#include "FileManager.h"
#include "ArduinoJson.h"

void Application::initDefaults()
{
  Serial.println("[Application]: Checking filesystem...");
  // Create ADHOC password file if not exists and setup ADHOC network.
  if(!FileManager::fileExists("/adhoc"))
    FileManager::writeFile("/adhoc", "H3LL0FR0MSL1M1IMaTesTAnDWILLB3ChanG3d");
}

void Application::initHardware()
{
  Camera::init();

  Serial.println("[Application]: Creating access point...");
  Network::createAccessPoint("WaifuFi™", (char*)FileManager::readFile("/adhoc").c_str());

  // Initialize the HTTP server before WIFI setup so server is bound to access point address. (192.168.4.1)
  Http::init();

  // Attempt to initialize previous wifi connection if found.
  Serial.println("[Application]: Checking WiFi...");
  bool connected =  Network::wifiConnect();
  if(Network::wifiProfileSet())
  {
    Serial.printf("[Application]: WiFI %s %s", connected ? "succesfully connected" : "failed to connect");
  } Serial.printf("[Application]: No WiFi profile found, skipping wifi initilization...");
  
}

void Application::setup()
{
  if(DEBUG)// Setup serial monitor if debug flag has been enabled.
    Serial.begin(115200); 
    
  Serial.println("[Application]: Starting device initalization...");
  Application::initDefaults();
  Application::initHardware();

  Serial.println("[Application]: Succesfully booted device.");
}

int currentTick = 0;
void Application::main()
{
  if(currentTick++ >= TICKS_REQUIRED)
  {
    if(Network::wifiConnected())
    {
      Serial.printf("[Application]: Currently logged in to wifi, IP: %s\n", Network::wifiIP().toString());
      if(API::IsAuthenticated())
        API::SendFrame();
    }
    else
    {
      
      Serial.println("[Application]: Wifi not connected, looking for wifi profile and nearby nearby connection");
    }

    currentTick -= TICKS_REQUIRED;
  }

  delay(TICK_IN_MS);
}