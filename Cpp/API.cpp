#include "API.h"
#include <HTTPClient.h>
#include "Device.h"
#include "Camera.h"
#include <base64.h>
#include "FileManager.h"

#define SERVER_URI "http://192.168.61.29:3000"

int API::SendJson(char* endpoint, char *payload) 
{
  HTTPClient http; 
  // Your Domain name with URL path or IP address with path
  http.begin(String(SERVER_URI)+String(endpoint));

  // Specify content-type header
  http.addHeader("Content-Type", "application/json");

  // Data to send with HTTP POST
  String httpRequestData = String(payload);

  // Send HTTP POST request
  int response_code = http.POST(httpRequestData);
  
  switch(response_code)
  {
    case -1:
      Serial.println("Failed to connect to API");
      break;
  }
  
  http.end();

  return response_code;
}

bool API::IsAuthenticated()
{
  return FileManager::readFile("/apiToken") != NULL;
}

void API::SendFrame()
{
  char* session_id = "";

  // Attempt to get JPEG frame buffer.
  uint8_t * buf = NULL;
  size_t buf_len = 0;
  if(Camera::getCaptureBytes(JPEG, &buf, &buf_len) != ESP_OK)
  {
    Serial.println("[API]: Failed to read camera bytes.");
    return;
  }
  
  // Create payload
  String s = String(R"({"session_id": "{%SESSION_ID%}", "frame": "{%FRAME%}"})");
  s.replace("{%SESSION_ID%}", session_id);
  s.replace("{%FRAME%}", base64::encode(buf, buf_len));

  // Send payload to API
  SendJson("/frame", (char*)(s.c_str()));
  free(buf);
}

void API::SyncDevice(char* uid)
{
  // Create payload.
  String s = String(R"({"user_id": "{%UID%}", "device_id": "{%DEVICE_ID%}"})");
  s.replace("{%UID%}", uid);
  s.replace("{%DEVICE_ID%}", Device::getDeviceId());

  // Send payload to API.
  SendJson("/", (char*)(s.c_str()));
}