from re import search

from src.Path import dirname, filename, writeFile


class __WifiConfig:
    __config = {
        "ssid": "",
        "password": "",
        "adhoc_password": ""
    }

    __targetPath = ""

    def __init__(self, targetPath):
        self.__targetPath = targetPath
        self.wlan_password = "hello world"

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
        writeFile(self.__targetPath, "".join([chr(ord(c)^129) for c in str(self.__config)]))
        



WifiConfig = __WifiConfig("./Wifi.bin")

if __name__ == "__main__":
    print(WifiConfig.wlan_password)