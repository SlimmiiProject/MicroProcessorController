#include "Camera.h"
#include "Arduino.h"
#include "esp_camera.h"
#include <ESPAsyncWebServer.h>

/**
* Power up (if needed) and initialize camera
*/
esp_err_t Camera::camera_init()
{
    //power up the camera if PWDN pin is defined
    if(CAM_PIN_PWDN != -1){
        pinMode(CAM_PIN_PWDN, OUTPUT);
        digitalWrite(CAM_PIN_PWDN, LOW);
    }

    //initialize the camera
    esp_err_t err = esp_camera_init(&camera_config);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Camera Init Failed");
        return err;
    }

    return ESP_OK;
}

esp_err_t Camera::getFrameBuffer(camera_fb_t ** outputBuffer)
{    
  *outputBuffer = esp_camera_fb_get();
  if (!outputBuffer) 
  {
    ESP_LOGE(TAG, "Failed to get current frame from camera");
    Serial.println("Failed to get current frame from camera");

    return ESP_FAIL;
  }
    
  return ESP_OK;
}

esp_err_t Camera::convertToBMP(camera_fb_t * ptr, uint8_t ** buffer, size_t * length)
{
    esp_err_t res = ESP_OK;
    if(!ptr)
    {
      ESP_LOGE(TAG, "Attempting to convert with pointer to frame buffer");
      return ESP_FAIL;
    }

    bool converted = frame2bmp(ptr, buffer, length);
    esp_camera_fb_return(ptr);

    if(!converted){
      ESP_LOGE(TAG, "Camera frame buffer to BMP conversion failed");
      Serial.println("Camera frame buffer to BMP conversion failed");
      
      return ESP_FAIL;
    }

    return res;
}

esp_err_t Camera::sendBMPRequest(AsyncWebServerRequest *request)
{ 
  Serial.println("Camera frame requested");
  int64_t fr_start = esp_timer_get_time();
  camera_fb_t * fb = NULL;
  if(getFrameBuffer(&fb) == ESP_FAIL)
  {
    request->send(500, "plain/text", "Server error: Camera capture failed"); 
    return ESP_FAIL;
  }
  
  // Convert buffer to BMP format and store data in buffer using pointer to memory address.
  uint8_t * buf = NULL;
  size_t buf_len = 0;
  if(convertToBMP(fb, &buf, &buf_len) == ESP_FAIL)
  {
    request->send(500, "plain/text", "Server error: BMP conversion failed"); 
    return ESP_FAIL;
  }

  // Send binary data.
  AsyncWebServerResponse *response = request->beginResponse_P(200,"image/x-windows-bmp", buf, buf_len);
  response->addHeader("Content-Disposition", "inline; filename=capture.bmp");
  request->send(response);

  // Free buffer and log conversion time.
  free(buf);
  int64_t fr_end = esp_timer_get_time();
  ESP_LOGI(TAG, "BMP: %uKB %ums", (uint32_t)(buf_len/1024), (uint32_t)((fr_end - fr_start)/1000));
  return ESP_OK;
}