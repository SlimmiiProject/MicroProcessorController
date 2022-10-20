/**
* Arduino ino ew run file. (better not to write code here, all ino files get concatenated based on alphabatical order, this results in unwanted bugs sometimes.)
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
