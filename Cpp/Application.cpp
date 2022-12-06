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
#define DEBUG 0

void Application::setup()
{

  Serial.begin(115200);  // Setup serial connection based on device upload speed.
  Camera::init();

  // Create ADHOC password file if not exists and setup ADHOC network.
  if(!FileManager::fileExists("/adhoc"))
    FileManager::writeFile("/adhoc", "H3LL0FR0MSL1M1IMaTesTAnDWILLB3ChanG3d");

  Network::createAccessPoint("WaifuFi™", (char*)FileManager::readFile("/adhoc").c_str());

  // Initialize the HTTP server before WIFI setup so 
  Http::init();

  // Deserialize the wifi JSON & log into WiFi.
  if(FileManager::fileExists("/wifi"))
  {

    const size_t CAPACITY = JSON_OBJECT_SIZE(1);
    StaticJsonDocument<CAPACITY> doc;
    deserializeJson(doc, (char*)FileManager::readFile("/wifi").c_str());

    JsonObject object = doc.as<JsonObject>();

    const char* ssid = object["ssid"];
    const char* password = object["password"];
    Network::wifiConnect((char*)ssid, (char*)password);
  }
  
  Serial.println("Succesfully booted device.");
}

void Application::main()
{
  if(Network::wifiIP().toString() != "0.0.0.0")
  {
    Serial.print("Currently logged in to wifi, IP:");
    Serial.println(Network::wifiIP());
    if(DEBUG)
    {
      API::SyncDevice("hello world");
      API::SendFrame();
    }
  } 
  delay(1000);
}