
from net.www.Webserver import Webserver
from src.net.Wifi import Wifi 
import uasyncio
import gc

gc.collect()


www = None
wifi = None


def __init():
    """
        Devicie initializiation 
    """
    # Gebruik globale variabele niet enkel in deze scope.
    global wifi
    global www

    # Initalizeer noodzakelijke componenten  
    www = Webserver(port=8080, maxClients=1)

    # Maakt WLAN en ADHOC connectie aan (Wifi/AccessPoint)
    wifi = Wifi()
    
async def __main():
    """
        Main device execution function
    """
    # Gebruik globale variabele niet enkel in deze scope.
    global wifi
    global www

    # Voeg de webserver start functie als task toe aan asyncio voor uit te voeren.
    uasyncio.create_task(www.start())
    uasyncio.create_task(__update())

    while True: # Loop main thread zodat het programma niet afsluit.
        await uasyncio.sleep_ms(10_000)

async def __update(): 
    """
        Reserved for device updates, wifi checks, etc...
    """
    while True:
        wifi.update()

# Main entry point, indien python interpeter naar dit bestand is gericht.
if __name__ == "__main__":
    __init()
    uasyncio.run(__main()) # Start main functie met async handler "uasyncio" => asyncio alternatief micropython.
