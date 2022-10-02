 
from re import search as searchPattern
from components.WifiSelector import WifiSelector

from net.www.WebserverRoute import WebserverRoute


class Routes:
    @WebserverRoute.get("/")
    def index(request, response):
        return response.render("/index")

    @WebserverRoute.get("/wifi")
    def wifi(request, response):
        return response.render("/wifi", **{
            "SSID_SELECTOR": WifiSelector("hello posted world"),
            "MESSAGE": "Failed to connect to wifi, please connect to a nearby access point"
        })

    @WebserverRoute.post("/wifi")
    def wifi(request, response):
        params = request.PARAMS
        message = "Wifi succesfully set."
        if not len(request.PARAMS):
            message = "Wifi not connected, please connect to a wifi access point."
        elif not all(i in params.keys() for i in ["ssid", "password"]):
            message = "Wifi SSID or password was not set"
        
        return response.render("/wifi", **{
            "SSID_SELECTOR": WifiSelector("hello posted world"),
            "MESSAGE": message
        })