from net.www.WebserverRoute import WebserverRoute
from components.layout.forms.WifiSelector import WifiSelector
from net.Wifi import Wifi
from utils.Device import Device
from net.WifiConfig import WifiConfig

class Routes:
    @WebserverRoute.get("/")
    def index(request, response):
    
        return response.getFile("/index") 
    
    @WebserverRoute.get("/wifi")
    def wifi(request, response):
        response.setParams(**{
            "MESSAGE": "Already connected to wifi network" if Wifi.wifi_connected else "No wifi network specified, or failed to connect",
            "SSID_SELECTOR": WifiSelector(*[network["ssid"] for network in Wifi.networks])
        })
        
        return response.getFile("/wifi") 
    
    @WebserverRoute.post("/wifi")
    def wifi(request, response):
        print(response.parameters)
        response.setParams(**{
            "MESSAGE": "Already connected to wifi network" if Wifi.wifi_connected else "No wifi network specified, or failed to connect",
            "SSID_SELECTOR": WifiSelector(*[network["ssid"] for network in Wifi.networks])
        })
        if all(key in response.parameters.keys() for key in ["ssid", "password"]):
            WifiConfig.wlan_ssid = response.parameters["ssid"]
            WifiConfig.wlan_password = response.parameters["password"]
            Device.hard_reset()
        
        return response.getFile("/wifi")
    
    @WebserverRoute.get("/change_adhoc")
    def adhoc(request, response):
        response.setParams(**{
            "MESSAGE": ""
        })
        return response.getFile("/change_adhoc") 
    
    @WebserverRoute.post("/change_adhoc")
    def adhoc(request, response):
        if any([i not in response.parameters.keys() for i in ["password_verify", "password"]]):
            response.setParams(MESSAGE="Invalid request")
        elif response.parameters["password"] != response.parameters["password_verify"]:
            response.setParams(MESSAGE="Password did not match")
        else:
            response.setParams(MESSAGE="ADHOC password changed succesfully")
            Device.hard_reset() 
        
        return response.getFile("/change_adhoc") 
    
    