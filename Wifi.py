import network
import os
import json

class Wifi: 
    wpa = None
    adhoc = None

    def __init__(self) -> None:
        self.wpa = self.CreateWPAInterface()
        self.adhoc = self.CreateADHOCInterface()
        
    def __connectionInfo(self): 
        """
            Load the connection information from the Wifi.bin file, or create if necessary 
        """
        # Creer wifi bestand indien nodig, gebruik XOR flip op karakters zodat data niet ruw wordt neergeschreven.
        # (close writer/reader, er is geen using in micropython anders blijft deze in memory)
        conInfoTemplate = """{"ssid":"ESP_000111", "password": "", "adhoc_password": "C0nn3ctT0Th3Sl1m1nn1M3t3rW1thTh1sP4ssw0rd"}"""
        if not "wifi.bin" in os.listdir("./"):
            writer = open("./wifi.bin", "x")
            writer.write("".join([chr(ord(i)^129) for i in conInfoTemplate]))
            writer.close()

        # Lees wifi bin bestand in terug met XOR flip om ze te herstellen.
        reader = open("./wifi.bin", "r")
        conInfo = json.loads("".join([chr(ord(i)^129) for i in reader.readline()]))
        reader.close()

        return conInfo

    def CreateWPAInterface(self):
        """
            Create WPA/WPAv2 connection interface (Wi-Fi protectec access)
        """
        conInfo = self.__connectionInfo()

        inf = network.WLAN(network.STA_IF)
        inf.active(True)
        inf.connect(conInfo["ssid"], conInfo["password"])
            
        return inf

    def CreateADHOCInterface(self):
        """
            Create AD-HOC connection interface (Access point)
        """
        conInfo = self.__connectionInfo()

        ap = network.WLAN(network.AP_IF)
        ap.config(essid="SlimmiiMeter", password=conInfo["adhoc_password"], max_clients=1)      

        ap.active(True)         

        return ap
    
    def update(self): 
        if self.wpa is None or not self.wlan.isconnected():
            wlan = wifi.CreateWPAInterface()
            
        if self.adhoc is None:
            wlan = wifi.CreateWPAInterface()

if __name__ == "__main__":
    wifi = Wifi()
    print("Output:")
    print(wifi.CreateADHOCInterface())
    inf = wifi.CreateWPAInterface()
    print(inf.isconnected())