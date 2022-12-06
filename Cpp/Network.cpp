#include <WiFi.h>
#include "Network.h"
#include "Arduino.h"

#define SLEEP_IN_MS 500
#define MAX_CONNECTION_ATTEMPTS 50

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

bool Network::wifiConnect(char *ssid, char *password)
{
  WiFi.begin(ssid, password);

  int attempt = 0;
  bool connected = false;
  while (!(connected = WiFi.status() == WL_CONNECTED) && attempt++ <= MAX_CONNECTION_ATTEMPTS) {
    delay(SLEEP_IN_MS);
  }

  return connected;
}

IPAddress Network::wifiIP() { return WiFi.localIP(); }
IPAddress Network::apIP()  { return WiFi.softAPIP(); }


bool Network::writeWifiProfile(NetworkProfile profile)
{
  return 0;
}