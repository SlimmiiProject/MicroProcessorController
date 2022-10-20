#include "http.h"
#include "Arduino.h"
#include <WiFi.h>

WiFiServer server;

void Http::init(uint16_t port)
{
  server = WiFiServer(port);
  server.begin();
}

void Http::handleClient(bool waitForConnect)
{
  do 
  {
    WiFiClient client = server.available();
    if(client)
    {
      Serial.println("Client connected");
      client.setNoDelay(true);
      while(client.connected())
      {
        if(client.available())
        { 
          Serial.println(client.readString());
          client.print("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\nHello World");
          
          client.stop();
        }
      }
      
      Serial.println("Client disconnected");
    }
  } while(waitForConnect);
}


