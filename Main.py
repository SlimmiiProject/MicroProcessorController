from asyncore import read
from glob import glob
from os import listdir
import uasyncio
import json

from Webserver import Webserver
from Wifi import Wifi 

wifi = None
www = None

def __init():
    # Gebruik globale variabele niet enkel in deze scope.
    global wifi
    global webserver

    # Creer wifi bestand indien nodig, gebruik XOR flip op karakters zodat data niet ruw wordt neergeschreven.
    # (close writer/reader, er is geen using in micropython anders blijft deze in memory)
    conInfo = """{"ssid":"", "password":""}"""
    if not "wifi.bin" in listdir("./"):
        writer = open("./wifi.bin", "x")
        writer.write("".join([chr(ord(i)^129) for i in conInfo]))
        writer.close()

    # Lees wifi bin bestand in terug met XOR flip om ze te herstellen.
    reader = open("./wifi.bin", "r")
    print(json.loads("".join([chr(ord(i)^129) for i in reader.readline()])))
    reader.close()

    # Initalizeer noodzakelijke componenten  
    wifi = Wifi(conInfo)
    www = Webserver(port=8080, maxClients=1)

    

async def __main():
    # Gebruik globale variabele niet enkel in deze scope.
    global wifi
    global webserver

    # Maakt WLAN en ADHOC connectie aan (Wifi/AccessPoint)
    wlan = wifi.CreateConnectionInterface()
    adhoc = wifi.CreateHotspotInterface()

    # Voeg de webserver start functie als task toe aan asyncio voor uit te voeren.
    uasyncio.create_task(www.start())
    while True:
        await uasyncio.sleep_ms(10_000)

# Main entry point, indien python interpeter naar dit bestand is gericht.
if __name__ == "__main__":
    __init()
    uasyncio.run(__main()) # Start main functie met async handler "uasyncio" => asyncio alternatief micropython.
