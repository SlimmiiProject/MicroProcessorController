#ifndef Network_h
#define Network_h
#include "Arduino.h" // Import arduino built-in lib for the class.
#include <WiFi.h>
#include <SPIFFS.h>
#include <vector>
#include <iostream>

typedef struct {
  char *ssid;
  char *password;
} NetworkProfile;

class Network 
{
  public: 
    /***
    * @description: Attempt to create a access point using {ssid}, {password} return setup succesfull in binary state
    * @returns: AP succesfully setup?
    */
    static bool createAccessPoint(char* ssid, char* password); 
    
    /***
    * @description: Attempt to connect to a router using {ssid}, {password} and return connected in binary state.
    * @returns: connected?
    */
    static bool wifiConnect(char* ssid, char* password);
  
    /***
    * @description: Write a wifi profile to the device 
    */
    static bool writeWifiProfile(NetworkProfile profile);

    /***
    * @description: Write a wifi profile to the device 
    */
    static NetworkProfile readNetworkProfile(char* path);

    /**
    * @description: The WiFi local IP Address 
    */
    static IPAddress wifiIP();
    
    /**
    * @description: The access point local IP
    */
    static IPAddress apIP();

    
};
#endif