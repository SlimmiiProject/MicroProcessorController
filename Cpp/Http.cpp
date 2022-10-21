#include "http.h"
#include "Arduino.h"
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <WiFi.h>

AsyncWebServer server(80);

// PROGMEM  => Store data in flash instead of SRAM, ram speed improvement due less bytes alocated in SRAM
// Probably should compress this in the future
const char page_css[] PROGMEM = R"rawliteral(
  :root { 
       --main-color: rgb(40, 71, 78); 
       --shadow-color: black; 
       --font-color: white; 
  }
  * { 
      margin: 0; 
      padding: 0;
  }
  body { 
      background-color: rgb(225, 225, 225);
  }
  body > header { 
      width: 100%; 
      height:5rem; 
      background-color: var(--main-color); 
  }
  body > header > span {
      font-size: 4rem; 
      padding: .5rem; 
      color: var(--font-color); 
      text-shadow: var(--shadow-color) 3px 3px;
  }
  
  main { 
      width: 90%; 
      margin: 0 auto; 
      display: block;
  }
  article *:nth-child(n + 2 ) { 
      padding: 1rem; 
  }
  article { 
      border: 2px solid var(--main-color);
      border-radius: 10px;
      margin: 1.6rem 0;
      background-color: white;
  }
  article > header { 
      background-color: var(--main-color);
      height: 2rem;
      display: flex;
      align-items: center; 
      color: var(--font-color); 
      font-weight: bold; 
      padding:0 1rem; 
      text-shadow: var(--shadow-color)  1px 1px; 
  }
)rawliteral";

const char page_html[] PROGMEM = R"rawliteral(
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link href="/style.css" type="text/css" rel="stylesheet">
</head>
<body>
    <header><span>Slimi</span></header>
    
    <main>
        <section>
            <article>
                <header>🗨&ensp;Reserved for possible title </header>
                <div class="content-container">
                    {%CONTENT%}
                </div>
            </article>
        </section>
    </main>
</body>
</html>
)rawliteral";


String Http::templateParser(const String& key)
{
  if (key == "WIFI_CONNECTED")
    return String("Wifi connected");
  else if(key == "WIFI_DISCONNECTED")
    return String("Wifi disconnected");
  
  return String("Component not found");
}

char* Http::getPageState()
{
  IPAddress wip = WiFi.localIP();
  if(wip.toString() == "0.0.0.0")
    return "%WIFI_DISCONNECTED%";
    
  return "%WIFI_CONNECTED%";
}

void Http::getPage(AsyncWebServerRequest *request) {
  String current_template = String(page_html);

  current_template.replace("{%CONTENT%}", getPageState());
  request->send_P(200, "text/html", current_template.c_str(), templateParser);
}

void Http::init()
{
  server.on("/", HTTP_GET, getPage );
  server.on("/style.css", HTTP_GET, [](AsyncWebServerRequest *request){ request->send(200, "text/css", page_css); });

  server.onNotFound([](AsyncWebServerRequest *request){  request->redirect("/"); });
  server.begin();
}

