#include "Device.h"
#include <Esp.h>

char* Device::getDeviceId() 
{
  char ssid[23];
  snprintf(ssid, 23, "MCUDEVICE-%llX", ESP.getEfuseMac());
  
  return ssid;
}