#include "Arduino.h"
#include <WiFi.h>
#include <SPIFFS.h>
#include "Network.h"

Network::Network() 
{
  sleep_in_ms = 500;
  max_connection_attempts = 50;
}

bool Network::createAccessPoint(char *ssid, char *password)
{
  WiFi.mode(WIFI_AP);
  
  int attempt = 0;
  bool connected = false;
  while(!(connected = WiFi.softAP(ssid, password)) && attempt++ < max_connection_attempts) {
    delay(sleep_in_ms);
  }

  return connected;
}

bool Network::wifiConnect(char *ssid, char *password)
{
  WiFi.begin(ssid, password);

  int attempt = 0;
  bool connected = false;
  while (!(connected = WiFi.status() == WL_CONNECTED) && attempt++ < max_connection_attempts) {
    delay(sleep_in_ms);
  }

  return connected;
}

IPAddress Network::wifiIP() { return WiFi.localIP(); }
IPAddress Network::apIP()  { return WiFi.softAPIP(); }

bool Network::writeWifiProfile(NetworkProfile profile)
{
  return 0;
}