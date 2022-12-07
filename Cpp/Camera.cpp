#include "Camera.h"
#include "Arduino.h"
#include "esp_camera.h"
#include <ESPAsyncWebServer.h>

esp_err_t Camera::init()
{
  Serial.println("[Camera]: Initializing camera...");
    //power up the camera if PWDN pin is defined
    if(CAM_PIN_PWDN != -1)
    {
        pinMode(CAM_PIN_PWDN, OUTPUT);
        digitalWrite(CAM_PIN_PWDN, LOW);
    }

    //initialize the camera
    esp_err_t err = esp_camera_init(&camera_config);
    if (err != ESP_OK) 
    {
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
    ESP_LOGE(TAG, "[Camera]: Failed to get current frame from camera");
    Serial.println("[Camera]: Failed to get current frame from camera");

    return ESP_FAIL;
  }
  
  return ESP_OK;
}

esp_err_t Camera::convertToBMP(camera_fb_t * ptr, uint8_t ** buffer, size_t * length)
{
    if(!ptr)
    {
      ESP_LOGE(TAG, "[Camera]: Attempting to convert with pointer to frame buffer");
      return ESP_FAIL;
    }

    bool converted = frame2bmp(ptr, buffer, length);
    esp_camera_fb_return(ptr);

    if(!converted)
    {
      ESP_LOGE(TAG, "[Camaera]: Camera frame buffer to BMP conversion failed");
      Serial.println("[Camera]: Camera frame buffer to BMP conversion failed");
      
      return ESP_FAIL;
    }

    return  ESP_OK;
}

esp_err_t Camera::convertToJPEG(camera_fb_t * frameBuffer, uint8_t ** buffer, size_t * length)
{
    if(!frameBuffer)
    {
      ESP_LOGE(TAG, "[Camera]: Attempting to convert with pointer to frame buffer");
      return ESP_FAIL;
    }

    if(frameBuffer->format == PIXFORMAT_JPEG)
    {
      *buffer = frameBuffer->buf;
      *length = frameBuffer->len;
    }
    else if (!frame2jpg(frameBuffer, camera_config.jpeg_quality, buffer, length))
    {
      ESP_LOGE(TAG, "[Camera]: Camera frame buffer to JPEG conversion failed");
      Serial.println("[Camera]: Camera frame buffer to JPEG conversion failed");
      return ESP_FAIL;
    }

    esp_camera_fb_return(frameBuffer);
    return ESP_OK;
}

esp_err_t Camera::getCaptureBytes(image_type type, uint8_t **bufferPtr, size_t * lengthPtr)
{
  int64_t fr_start = esp_timer_get_time();
  camera_fb_t * fb = NULL;
  if(getFrameBuffer(&fb) == ESP_FAIL)
    return ESP_FAIL;

  esp_err_t res = ESP_OK;
  switch(type)
  {
    case JPEG: 
      if(convertToJPEG(fb, bufferPtr, lengthPtr) != ESP_OK)
        res = ESP_FAIL;
      break;
    case BMP: 
      if(convertToBMP(fb, bufferPtr, lengthPtr) != ESP_OK)
        res = ESP_FAIL;
      break;
    
    default: res = ESP_FAIL; 
  }

  esp_camera_fb_return(fb);
  
  return res; 
}
