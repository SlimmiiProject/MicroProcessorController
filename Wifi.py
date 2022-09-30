import network
import os

class Wifi: 
    __connectionInfo = None
    def __init__(self, connectionInfo) -> None:
        self.__connectionInfo = connectionInfo

    def CreateConnectionInterface(self):

        inf = network.WLAN(network.STA_IF)
        inf.active(True)
        inf.connect(self.__connectionInfo["ssid"], self.__connectionInfo["password"])
            
        return inf

    def CreateHotspotInterface(self):
        # Create access point interface
        ap = network.WLAN(network.AP_IF) # create access-point interface
        ap.config(ssid='SlimmiiMeter') # set the SSID of the access point
        ap.config(max_clients=1) # set how many clients can connect to the network
        
        ap.active(True)         # activate the interface

        return ap

if __name__ == "__main__":
    wifi = Wifi()
    print("Output:")
    print(wifi.CreateHotspotInterface("Digitale-Meter"))
    inf = wifi.CreateConnectionInterface("ESP_000111", None)
    print(inf.isconnected())