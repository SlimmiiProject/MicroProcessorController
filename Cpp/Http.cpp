#include "Http.h"
#include "Arduino.h"
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <WiFi.h>
#include "Camera.h"
#include "Network.h"
#include <base64.h>
#include "FileManager.h"

AsyncWebServer server(80);  

/**
* Component loader.
*/
char* Http::templateParser(const String& key)
{
  if (key == "WIFI_CONNECTED")
    return (char*)DASHBOARD;
  else if(key == "WIFI_DISCONNECTED")
    return (char*)LOGIN_FORM;
  
  return "";
}

/**
* Page state parser.
*/
char* Http::getPageState()
{
  /**
  * Fetch the content template name to build content for.
  */
  IPAddress wip = WiFi.localIP();
  if(wip.toString() == "0.0.0.0")
    return "%WIFI_DISCONNECTED%";
    
  return "%WIFI_CONNECTED%";
}

void Http::getPage(AsyncWebServerRequest *request) 
{
  String current_template = String(page_html);

  current_template.replace("{%CONTENT%}", getPageState());
  request->send_P(200, "text/html", current_template.c_str(), templateParser);
}

void Http::wifiLogin(AsyncWebServerRequest *request) {
  // Has params function doesnt work for some reason, gotta look into this, temorary include check.
  char* ssid = "";
  char* password = "";
  for(int i = 0; i < request->params(); i++)
  {
    char* value = (char*)request->getParam(i)->value().c_str();
    if(request->getParam(i)->name().indexOf("ssid") >= 0)
      ssid = value;
    else if(request->getParam(i)->name().indexOf("password") >= 0)
      password = value;
  }
  
  if(strlen(ssid) > 0 && strlen(password) > 0)
  {
    Serial.println("Connecting to wifi");
    String s = String(R"({"ssid": "{%SSID%}", "password": "{%PASSWORD%}"})");
    s.replace("{%SSID%}", ssid);
    s.replace("{%PASSWORD%}", password);

    FileManager::writeFile("/wifi", (char*)s.c_str());
    Network::wifiConnect(ssid, password);
  }


  String current_template = String(page_html);

  current_template.replace("{%CONTENT%}", getPageState());
  request->send_P(200, "text/html", current_template.c_str(), templateParser);
}

void Http::updateSettings(AsyncWebServerRequest *request) {
  // Has params function doesnt work for some reason, gotta look into this, temorary include check.
  char* accessPassword = "";
  char* apiKey = "";

  // Request getparam => name didnt work for some reason.
  for(int i = 0; i < request->params(); i++)
  {
    char* value = (char*)request->getParam(i)->value().c_str();
    if(request->getParam(i)->name().indexOf("adhocPassword") >= 0)
      accessPassword = value;
    else if(request->getParam(i)->name().indexOf("userKey") >= 0)
      apiKey = value;
  }

  if(strlen(accessPassword))
    FileManager::writeFile("/adhoc", accessPassword);

  FileManager::writeFile("/apiToken", apiKey);

  request->redirect("/");
}


void Http::sendImage(AsyncWebServerRequest *request)
{
  // Get camera buffer and camera buffer length.
  uint8_t * buf = NULL;
  size_t buf_len = 0;
  if(Camera::getCaptureBytes(JPEG, &buf, &buf_len) != ESP_OK)
  {
    Serial.println("Image request received, failed to capture camera bytes.");
    request->send(500, "plain/text", "Server error: Failed to get camera bytes"); 
    return;
  }

  // Send buffer (length) as image/JPEG mime.
  AsyncWebServerResponse *response = request->beginResponse_P(200,"image/jpeg", buf, buf_len);
  response->addHeader("Content-Disposition", "inline; filename=capture.jpg");
  request->send(response);

  // deallocate buffer bytes.
  free(buf);
}


void Http::logout(AsyncWebServerRequest *request)
{
  Network::wifiDisconnect();
  request->redirect("/");
}

void Http::init()
{
  Serial.println("[Http]: Initializing HTTP server");
  // Assign endpoints.
  server.on("/", HTTP_GET, Http::getPage );
  server.on("/", HTTP_POST, Http::wifiLogin );
  server.on("/disconnect", HTTP_GET, Http::logout );
  server.on("/updateSettings", HTTP_POST, Http::updateSettings );

  server.on("/style.css", HTTP_GET, [](AsyncWebServerRequest *request){ request->send(200, "text/css", page_css); });
  server.on("/capture.jpg", HTTP_GET, sendImage);
  //server.on("/capture", HTTP_GET, sendImageStream);
  server.onNotFound([](AsyncWebServerRequest *request){  request->redirect("/"); });

  // Start server.
  server.begin();
}

