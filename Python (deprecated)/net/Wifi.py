import os
import json
import network
from net.WifiConfig import WifiConfig
from utils.Logger import print_log, print_error
from time import sleep

class __Wifi: 
    __wpa = None
    __adhoc = None
    __max_attempts = 3
    
    def __init__(self):
        print_log(self, "Initializing network interface...")
        self.__wpa = self.__CreateWPAInterface()

        self.__wpa.scan()
        if WifiConfig.wlan_ssid in [network["ssid"] for network in self.networks]:
            print_log(self, "Found previous connected wifi network, connecting to: {SSID}".format(SSID=WifiConfig.wlan_ssid))
            
            for i in range(0, self.__max_attempts):
                try:
                    self.connect()
                    sleep(.75)
                    
                    if self.wifi_connected:
                        print_log(self, "Wifi connection established assigned ip: {IP}".format(IP=self.ip_adress))
                        break
                    elif i == self.__max_attempts-1:
                        raise(OSError())
                    
                except OSError:
                     print_error(self, "Failed to connect to network...")

        else:
             print_log(self, "No previous networks found")
             
        self.__adhoc = self.__CreateADHOCInterface()
            
        

    def __CreateWPAInterface(self):
        """
            Create WPA/WPAv2 connection interface (Wi-Fi protectec access)
        """

        inf = network.WLAN(network.STA_IF)
        inf.active(True)
        
        return inf

    def __CreateADHOCInterface(self, ip = '192.168.4.1', subnet =  '255.255.255.0', gateway = '192.168.4.1', dns = '8.8.8.8'):
        """
            Create AD-HOC connection interface (Access point)
        """

        ap = network.WLAN(network.AP_IF)
        ap.config(essid="SlimmiiMeter", password=WifiConfig.adhoc_password)
        ap.ifconfig((ip, subnet, gateway, dns))
        ap.active(True)      

        return ap

    @property
    def ip_adress(self):
        return self.__wpa.ifconfig()[0] if self.wifi_connected else None
    
    @property
    def wifi_connected(self):
        return self.__wpa.isconnected()
    
    @property
    def adhoc_ip_adress(self):
        return self.__adhoc.ifconfig()[0] if self.__adhoc else None
    
    @property
    def networks(self):
        return [{
             "ssid": ssid.decode("utf-8"),
             "bssid": bssid,
             "channel": channel,
             "rssi": RSSI,
             "security": security,
             "hidden": hidden
        } for ssid, bssid, channel, RSSI, security, hidden in self.__wpa.scan()]
    
    def connect(self):
        return self.__wpa.connect(WifiConfig.wlan_ssid, WifiConfig.wlan_password)
    
    def reset_adhoc(self):
        addr = self.__adhoc.ifconfig()
        self.__adhoc = self.__CreateADHOCInterface(*addr)
        
Wifi = __Wifi()
