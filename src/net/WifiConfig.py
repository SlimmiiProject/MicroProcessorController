from re import search
from utils.Path import dirname, filename, writeFile, readFileLine, file_exists
from utils.Crypt import XOR
import json


class __WifiConfig:
    __config = {
        "ssid": "",
        "password": "",
        "adhoc_password": "Sl1m1m3t3rP4ssw0rdF0rC0nnection"
    }

    __targetPath = ""

    def __init__(self, targetPath):
        self.__targetPath = targetPath
        self.__readFile()
        

    @property
    def wlan_ssid(self):
        return self.__config["ssid"]

    @wlan_ssid.setter
    def wlan_ssid(self, value):
        assert isinstance(value, str)

        self.__config["ssid"] = value
        self.__updateFile()

    @property
    def wlan_password(self):
        return self.__config["password"]

    @wlan_password.setter
    def wlan_password(self, value):
        assert isinstance(value, str)

        self.__config["password"] = value
        self.__updateFile()

    @property
    def adhoc_password(self):
        return self.__config["adhoc_password"]

    @adhoc_password.setter
    def adhoc_password(self, value):
        assert isinstance(value, str)

        self.__config["adhoc_password"] = value
        self.__updateFile()

    def __updateFile(self):
        writeFile(self.__targetPath, XOR(json.dumps(self.__config)))
        
    def __readFile(self):
        print()
        if file_exists(self.__targetPath):
            file_data = XOR(readFileLine(self.__targetPath))
            self.__config = json.loads(file_data)

         
        



WifiConfig = __WifiConfig("/Wifi.bin")

