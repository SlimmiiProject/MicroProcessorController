from os import listdir
import random
import sys
import machine
import ubinascii
from Enviroment import Enviroment
from utils.Logger import Logger

class __Device: 
    def __init__(self):
        if not hasattr(machine, "unique_id"):
            raise(OSError("Unable to detect hardware id"))

    @property
    def serial_no(self):
        return ubinascii.b2a_base64(machine.unique_id())

    def soft_reset(self):
        sys.exit()

    def hard_reset(self):
        machine.reset()
        
    async def update(self): 
        """
            Attempt to assign the LED pin id's, if invalid_pin, ignore the pin otherwise set to update queue
            if any pins have been loaded, update pin state using pin callback.
        """
        pins = []
        setters = [(Enviroment.WIFI_LED_PIN, lambda pin: pin.value(int(Wifi.wifi_connected))), (Enviroment.ADHOC_LED_PIN, lambda pin: pin.value(int(Wifi.adhoc_ip_adress is not None)))]
        for id, callback in setters:
            newVal = None
            try:
                newVal = (machine.Pin(id, machine.Pin.OUT), callback)
            except ValueError as e:
                if e.errno == "invalid pin":
                    if id == Enviroment.WIFI_LED_PIN:
                        Logger.error(self, "Failed to setup wifi led pin: (Invalid enviroment -> WIFI_LED_PIN value)")
                    elif id == Enviroment.ADHOC_LED_PIN:
                        Logger.error(self, "Failed to setup adhoc led pin: (Invalid enviroment -> ADHOC_LED_PIN value)")
                elif Enviroment.DEBUG_MODE:
                    raise(e)
            finally: 
                if newVal is not None:
                    pins.append(newVal)
                    
        del(setters) # Remove setter stack, possibly chugs up memory due occasional infinite loop
        while len(pins):
            for pin, callback in pins:
                callback(pin)
                
            await uasyncio.sleep_ms(1000)
    

Device = __Device()