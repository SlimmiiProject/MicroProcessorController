import network
import os

class Wifi: 
    """
        Wifi interface, gebruik voor aanmaken access point en conn interface. 
    """
    @staticmethod
    def CreateConnectionInterface(ssid, password):
        inf = network.WLAN(network.STA_IF)
        inf.active(True)
        inf.connect(ssid, password)
            
        return inf

    @staticmethod
    def CreateHotspotInterface(ssid):
        # Create access point interface
        ap = network.WLAN(network.AP_IF) # create access-point interface
        # ap.config(ssid='ESP-AP') # set the SSID of the access point
        # ap.config(max_clients=10) # set how many clients can connect to the network
        ap.active(True)         # activate the interface

        return ap

if __name__ == "__main__":
    print("Output:")
    print(Wifi.CreateHotspotInterface("Digitale-Meter"))
    inf = Wifi.CreateConnectionInterface("ESP_000111", None)
    print(inf.isconnected())