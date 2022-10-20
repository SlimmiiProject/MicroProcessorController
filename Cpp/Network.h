#ifndef Network_h
#define Network_h
#include "Arduino.h" // Import arduino built-in lib for the class.
#include <WiFi.h>
#include <SPIFFS.h>

typedef struct {
  char *ssid;
  char *password;
} NetworkProfile;

class Network 
{
  private: 
    /** @description: Max tries for making an access point or connection */
    uint8_t max_connection_attempts;

    /** @description: Time to sleep between network attempt actions */
    unsigned short int sleep_in_ms;
  
  public: 
    /** @description: class constructor, initializes the {max_connection_attempts} and {sleep_in_ms} variables. */
    Network(); 

    /***
    * @description: Attempt to create a access point using {ssid}, {password} return setup succesfull in binary state
    * @returns: AP succesfully setup?
    */
    bool createAccessPoint(char* ssid, char* password); 
    
    /***
    * @description: Attempt to connect to a router using {ssid}, {password} and return connected in binary state.
    * @returns: connected?
    */
    bool wifiConnect(char* ssid, char* password);
  
    /***
    * @description: Write a wifi profile to the device 
    */
    bool writeWifiProfile();

    /**
    * @description: The WiFi local IP Address 
    */
    IPAddress wifiIP();
    
    /**
    * @description: The access point local IP
    */
    IPAddress apIP();
};
#endif