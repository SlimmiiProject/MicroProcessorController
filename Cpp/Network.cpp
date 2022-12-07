#include <WiFi.h>
#include "Network.h"
#include "Arduino.h"
#include "ArduinoJson.h"
#include "FileManager.h"

#define SLEEP_IN_MS 500
#define MAX_CONNECTION_ATTEMPTS 50
#define WIFI_PROFILE_PATH "/wifi"

bool Network::createAccessPoint(char * ssid, char * password)
{
  WiFi.mode(WIFI_AP);
  
  bool connected = false;
  for(int currentAttempt = 0; currentAttempt < MAX_CONNECTION_ATTEMPTS && !connected; currentAttempt++)
  {
    connected = WiFi.softAP(ssid, password);
    delay(SLEEP_IN_MS);
  }

  Serial.print("Wifi state: ");
  Serial.println(String(connected ? "C" : "Disc")+"onnected");

  return connected;
}

bool Network::wifiConnected()
{
  return Network::wifiIP().toString() != "0.0.0.0";
}

bool Network::wifiProfileSet()
{
  return FileManager::fileExists("/wifi");
}

bool Network::wifiConnect()
{
  NetworkProfile profile = Network::readNetworkProfile();
  return Network::wifiConnect(profile.ssid, profile.password);
}

bool Network::wifiConnect(char *ssid, char *password)
{
  String ssid_normalized = String(ssid);
  ssid_normalized.trim();

  String wlan_password = String(password);
  wlan_password.trim();

  int attempt = 0;
  bool connected = false;
  while (!(connected = WiFi.status() == WL_CONNECTED) && attempt++ <= MAX_CONNECTION_ATTEMPTS) {
    WiFi.begin((char*)ssid_normalized.c_str(), (char*)wlan_password.c_str());
    delay(SLEEP_IN_MS);
  }

  return connected;
}

IPAddress Network::wifiIP() { return WiFi.localIP(); }
IPAddress Network::apIP()  { return WiFi.softAPIP(); }


bool Network::writeWifiProfile(char* ssid, char* password)
{
  String s = String(R"({"ssid": "{%SSID%}", "password": "{%PASSWORD%}"})");
  s.replace("{%SSID%}", ssid);
  s.replace("{%PASSWORD%}", password);

  return FileManager::writeFile("/wifi", (char*)s.c_str());
}

NetworkProfile Network::readNetworkProfile()
{
  NetworkProfile netProfile;
  if(FileManager::fileExists("/wifi"))
  {
    const size_t CAPACITY = JSON_OBJECT_SIZE(2);
    StaticJsonDocument<CAPACITY> doc;
    deserializeJson(doc, (char*)FileManager::readFile("/wifi").c_str());

    JsonObject object = doc.as<JsonObject>();

    const char* ssid = object["ssid"];
    const char* password = object["password"];

    netProfile.ssid = (char*)ssid;
    netProfile.password = (char*)password;


  }
  return netProfile;
}
