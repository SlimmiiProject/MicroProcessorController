
from net.www.Webserver import Webserver
import uasyncio
import machine
import gc

gc.collect()


www = None


def __init():
    """
        Devicie initializiation 
    """
    # Gebruik globale variabele niet enkel in deze scope.
    global www
    # Initalizeer noodzakelijke componenten  
    www = Webserver(port=80, maxClients=1)
    # Maakt WLAN en ADHOC connectie aan (Wifi/AccessPoint)
    
async def __main():
    """
        Main device execution function
    """
    # Gebruik globale variabele niet enkel in deze scope.
    global www

    loop = uasyncio.get_event_loop()
    
    # Voeg de webserver start functie als task toe aan asyncio voor uit te voeren.
    loop.create_task(www.start())
    loop.create_task(__update())
    
    loop.run_forever()
            

async def __update(): 
    """
        Reserved for device updates, wifi checks, etc...
    """
    
    wifi_pin =  machine.Pin(16, machine.Pin.OUT)
    adhoc_pin =  machine.Pin(17, machine.Pin.OUT)
    while True:
        if Wifi.adhoc_ip_adress is not None:
            adhoc_pin.value(1)
        if Wifi.wifi_connected:
            wifi_pin.value(1)
            
        await uasyncio.sleep_ms(1000)

# Main entry point, indien python interpeter naar dit bestand is gericht.
if __name__ == "__main__":
    power_pin = machine.Pin(0, machine.Pin.OUT)
    power_pin.value(1)

    from net.Wifi import Wifi 
    try:
        __init()
        uasyncio.run(__main()) # Start main functie met async handler "uasyncio" => asyncio alternatief micropython.

    except OSError as e:
        if e.errno == 98:
            machine.reset()
            
        print(e)
