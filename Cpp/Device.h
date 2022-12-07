#ifndef DEVICE_H
#define DEVICE_H

class Device 
{
  public:
    /** @description: Get the device serial number. */
    static char* getDeviceId();
};

#endif