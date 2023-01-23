#ifndef Network_h
#define Network_h
#include "Arduino.h" // Import arduino built-in lib for the class.
#include <WiFi.h>
#include <SPIFFS.h>
#include <vector>
#include <iostream>

#define WIFI_CONFIG_PATH "/wifi"

typedef struct {
  char *ssid;
  char *password;
} NetworkProfile;


class Network 
{
  private:
    /***
    * @description: Read the last connected wifi profile of the device.
    */
    static NetworkProfile readNetworkProfile();

  public: 
    /***
    * @description: Attempt to create a access point using {ssid}, {password} return setup succesfull in binary state
    * @returns: AP succesfully setup?
    */
    static bool createAccessPoint(char* ssid, char* password); 
    
    /**
    * @description: Attempt to connect to a router using the saved network profile and return connected in binary state.
    * @returns: connected?
    */
    static bool wifiConnect();

    /***
    * @description: Attempt to connect to a router using {ssid}, {password} and return connected in binary state.
    * @returns: connected?
    */
    static bool wifiConnect(char* ssid, char* password);

    static void wifiDisconnect();

    /***
    * @description: Checks or the current wifiIP is set to the local gateway address, rturns true if not set to that address.
    * @returns: Connected?
    */
    static bool wifiConnected();
  
    /***
    * @description: Write a network profile to the device.
    */
    static bool writeWifiProfile(char* ssid, char* password);

    /***
    * @description: WiFi profile set?
    */
    static bool wifiProfileSet();


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