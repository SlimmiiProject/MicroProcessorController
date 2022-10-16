
from net.www.Webserver import Webserver
from Enviroment import Enviroment
from utils.Logger import Logger
from utils.Device import Device
import uasyncio
import machine

www = None

# https://github.com/lemariva/micropython-camera-driver
def __init():
    """
        Device initializiation 
    """
    
    global www
    www = Webserver(port=80, maxClients=1)

async def __main():
    """
        Main device execution function
    """
    global www

    loop = uasyncio.get_event_loop()

    await loop.create_task(Device.update())
    await loop.create_task(www.start())
    
    loop.run_forever()
            

# Main entry point, indien python interpeter naar dit bestand is gericht.
if __name__ == "__main__":
    from net.Wifi import Wifi 
    try:
        __init()
        uasyncio.run(__main()) # Start main functie met async handler "uasyncio" => asyncio alternatief micropython.
    
    except OSError as e:
        Logger.error("main", f"An exception occured: {e}")
 
        if Enviroment.DEBUG_MODE:
            if e.errno == 98:
                machine.reset()
            else:
                raise(e)