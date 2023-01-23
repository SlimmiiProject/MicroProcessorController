/**
* Arduino ino ew run file. (better not to write code here, all ino files get concatenated based on alphabatical order, this results in unwanted bugs sometimes.)
*
*/
#include <WiFi.h>
#include "Application.h"
#include "Network.h"

#define MS_PER_TICK 1000
#define MIN_TICK 10

void setup() 
{
  Application::setup();

  Serial.printf("Wifi profile: %s\n", Network::wifiProfileSet() ? "Set" : "Not found");
}

void loop() {
  Application::main();
}
