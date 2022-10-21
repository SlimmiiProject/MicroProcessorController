/**
* Arduino ino ew run file. (better not to write code here, all ino files get concatenated based on alphabatical order, this results in unwanted bugs sometimes.)
*
*  Required libraries: 
* - https://github.com/espressif/esp32-camera
* - https://github.com/me-no-dev/ESPAsyncWebServer
* - https://github.com/me-no-dev/AsyncTCP
*/

#include <WiFi.h>
#include "Application.h"

Application app; 
void setup() 
{
  app.setup();
}

void loop() {
  app.main();
}
