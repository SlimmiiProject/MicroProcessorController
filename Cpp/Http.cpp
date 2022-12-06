#include "http.h"
#include "Arduino.h"
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <WiFi.h>
#include "Camera.h"
#include "Network.h"
#include <base64.h>
#include "FileManager.h"

AsyncWebServer server(80);  

char* Http::templateParser(const String& key)
{
  if (key == "WIFI_CONNECTED")
    return "Connected to wifi";
  else if(key == "WIFI_DISCONNECTED")
    return (char*)LOGIN_FORM;
  else if(key == "NETWORKS")
  {
    char* content = "";
    for(int i = 0; i < WiFi.scanNetworks(true); i++)
    {

      Serial.println(WiFi.SSID(i));
      delay(50);
    }
    WiFi.scanDelete();
    return content;
  } 
  
  return "";
}

char* Http::getPageState()
{
  /**
  * Fetch the content template name to build content for.
  */
  IPAddress wip = WiFi.localIP();
  if(wip.toString() == "0.0.0.0")
    return "%WIFI_DISCONNECTED%";
    
  return "%WIFI_DISCONNECTED%";//"%WIFI_CONNECTED%";
}

void Http::getPage(AsyncWebServerRequest *request) {
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

/*
void Http::sendImageStream(AsyncWebServerRequest *request)
{
  esp_err_t res = ESP_OK;

  uint8_t * buf = NULL;
  size_t buf_len = 0;
  if(Camera::getCaptureBytes(JPEG, &buf, &buf_len) != ESP_OK)
  {
    res = ESP_FAIL;
    request->send(500, "plain/text", "Server error: Failed to get camera bytes"); 
    return;
  }

    int i= 10;
    AsyncWebServerResponse *response = request->beginChunkedResponse("text/plain", [](uint8_t *buffer, size_t maxLen, size_t index) -> size_t {
      Serial.println("index"); 
      return 0;
    });

    response->addHeader("Content-Type","multipart/x-mixed-replace;boundary=123456789000000000000987654321");
    request->send(response);
}
*/

void Http::init()
{
  // Assign endpoints.
  server.on("/", HTTP_GET, Http::getPage );
  server.on("/", HTTP_POST, Http::wifiLogin );

  server.on("/style.css", HTTP_GET, [](AsyncWebServerRequest *request){ request->send(200, "text/css", page_css); });
  server.on("/capture.jpg", HTTP_GET, sendImage);
  //server.on("/capture", HTTP_GET, sendImageStream);
  server.onNotFound([](AsyncWebServerRequest *request){  request->redirect("/"); });

  // Start server.
  server.begin();
}

