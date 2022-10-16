import gc
from machine import Pin
from Enviroment import Enviroment
from utils.Logger import Logger

# Enable garbage collection
gc.collect()

# Enable power out
try:
    power_pin = Pin(Enviroment.POWER_LED_PIN, Pin.OUT)
    power_pin.value(1)
except ValueError as e:
    if e.errno == "invalid pin":
        Logger.error("boot", "Failed to setup power pin: (Invalid enviroment -> POWER_LED_PIN value)")
    else:
        if Enviroment.DEBUG_MODE:
            raise(e)
        else:
            Logger.error("boot", f"Failed to setup power pin unkown error: {e}")

from net.Wifi import Wifi 
