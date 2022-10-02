import network
import os
import json

class Wifi: 
    __wpa = None
    __adhoc = None

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
        try:
            #if self.__wpa is None or not self.__wpa.isconnected():
            #    self.__wpa = self.CreateWPAInterface()

            if self.__adhoc is None:
                self.__adhoc = self.CreateADHOCInterface()

            if self.__wpa is None:
                self.__wpa = self.CreateWPAInterface()
                print(self.__wpa.scan())

            
        except OSError as e:
            print(e)