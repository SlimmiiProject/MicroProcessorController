#ifndef Http_h
#define Http_h 
#include "Arduino.h"
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <WiFi.h>
#include "Camera.h"
#include "Network.h"

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

  form 
  {
    display: flex; 
    justify-content: center;
    flex-direction: column;
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
    <META HTTP-EQUIV="Refresh" CONTENT=I>
</head>
<body>
    <header><span>Slimmi</span></header>
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

const char LOGIN_FORM[] PROGMEM = R"rawliteral(
  <form method="POST">
      <label for="ssid">SSID:</label>
      <input type="text" name="ssid" id="ssid" />

      <label for="password">Password</label>
      <input type="password" name="password" id="password" />

      <input type="submit" value="Login" />
    </form>
)rawliteral";

/***
* @description: Http server handling class with master page implementation. 
*/
class Http
{
  public: 
    /** @description: Initialize the HTTP server. */
    static void init();
  
  private:
    /** 
    * @description: Replace the {%CONTENT%} variable with the current page state on the master page and serve the page using the template parser.
    *
    * @param request A pointer to the request callback.
    */
    static void getPage(AsyncWebServerRequest *request);

    /**
    * @description: Get the current state of the device and fetch the correct parameter for the template parser.
    */
    static char* getPageState();


    static char* templateParser(const String& key);

    /**
    * 
    */
    static void sendImage(AsyncWebServerRequest *request);
    static void sendImageStream(AsyncWebServerRequest *request);
    static void wifiLogin(AsyncWebServerRequest *request);
};
#endif
