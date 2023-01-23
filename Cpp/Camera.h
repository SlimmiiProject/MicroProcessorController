#ifndef CAMERA_H
#define CAMERA_H
#include "Arduino.h"
#include "esp_camera.h"
#include <ESPAsyncWebServer.h>

// Camera IO pins
#define CAM_PIN_PWDN -1   //power down is not used
#define CAM_PIN_RESET -1  //software reset will be performed
#define CAM_PIN_XCLK 21
#define CAM_PIN_SIOD 26
#define CAM_PIN_SIOC 27

#define CAM_PIN_D7 35
#define CAM_PIN_D6 34
#define CAM_PIN_D5 39
#define CAM_PIN_D4 36
#define CAM_PIN_D3 19
#define CAM_PIN_D2 18
#define CAM_PIN_D1 5
#define CAM_PIN_D0 4
#define CAM_PIN_VSYNC 25
#define CAM_PIN_HREF 23
#define CAM_PIN_PCLK 22

// Output pixel formats
enum image_type {
  JPEG = 0,
  BMP = 1
};

// Set configuration (pins, channels, camera rendering specifications)
// Format: VGA (640x480)
// PixeFormat: Grayscale
// Quality weight: 12/63
// Camera freq: 20mhz
static camera_config_t camera_config = {
  .pin_pwdn = CAM_PIN_PWDN,
  .pin_reset = CAM_PIN_RESET,
  .pin_xclk = CAM_PIN_XCLK,
  .pin_sccb_sda = CAM_PIN_SIOD,
  .pin_sccb_scl = CAM_PIN_SIOC,

  .pin_d7 = CAM_PIN_D7,
  .pin_d6 = CAM_PIN_D6,
  .pin_d5 = CAM_PIN_D5,
  .pin_d4 = CAM_PIN_D4,
  .pin_d3 = CAM_PIN_D3,
  .pin_d2 = CAM_PIN_D2,
  .pin_d1 = CAM_PIN_D1,
  .pin_d0 = CAM_PIN_D0,
  .pin_vsync = CAM_PIN_VSYNC,
  .pin_href = CAM_PIN_HREF,
  .pin_pclk = CAM_PIN_PCLK,

  .xclk_freq_hz = 16000000,
  .ledc_timer = LEDC_TIMER_0,
  .ledc_channel = LEDC_CHANNEL_0,

  .pixel_format = PIXFORMAT_GRAYSCALE,
  .frame_size = FRAMESIZE_VGA,

  .jpeg_quality = 12,
  .fb_count = 1,
  .grab_mode = CAMERA_GRAB_WHEN_EMPTY
};


class Camera {
  public:
    /** 
      * @description: Power up if required (powerpin != -1) and initialize the camera. 
      */
    static esp_err_t init();

    /** 
      * @description: Convert a frame buffer to a pixel format and allocate the {buffer} and {length} to the memory address specified as parameter.
      *
      * @param type The pixelformat type of the output types
      * @param bufferPtr a pointer to the reference of the capture bytes.
      * @param lengthPtr a pointer to the size of the bytes captured from the camera.
      */
    static esp_err_t getCaptureBytes(image_type type, uint8_t **bufferPtr, size_t *lengthPtr);


  private:
    /**
      * @description: Try to get current camera frame buffer and allocate to a memory address specified as {outputBuffer} parameter.
      *
      * @param outputBuffer The pointer to store the frame buffer object to.
      */
    static esp_err_t getFrameBuffer(camera_fb_t **outputBuffer);

    /** 
      * @description: Convert a frame buffer to BMP pixel format and allocate the {buffer} and {length} to the memory address specified as parameter 
      *
      * @param frameBufferPtr a pointer to the frame buffer object 
      * @param pixelDataBuffer a reference to the pointer of captured frame buffer
      * @param pixelDataBufferLength a pointer to the captured frame buffer length
      */
    static esp_err_t convertToBMP(camera_fb_t *frameBufferPtr, uint8_t **pixelDataBuffer, size_t *pixelDataBufferLength);

    /** 
      * @description: Convert a frame buffer to JPEG pixel format and allocate the {buffer} and {length} to the memory address specified as parameter  
      *
      * @param frameBufferPtr a pointer to the frame buffer object 
      * @param pixelDataBuffer a reference to the pointer of captured frame buffer
      * @param pixelDataBufferLength a pointer to the captured frame buffer length
      */
    static esp_err_t convertToJPEG(camera_fb_t *frameBufferPtr, uint8_t **pixelDataBuffer, size_t *pixelDataBufferLength);
};
#endif