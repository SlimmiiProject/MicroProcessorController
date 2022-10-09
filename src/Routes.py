 
from re import search as searchPattern

from components.scripts.Redirect import Redirect
from components.layout.forms.WifiSelector import WifiSelector
from net.www.WebserverRoute import WebserverRoute
from net.Wifi import Wifi


class Routes:
    @WebserverRoute.get("/")
    def index(request, response):
        return response.send(Redirect("/wifi", 0))
        return response.render("/index")

    @WebserverRoute.get("/wifi")
    def wifi_get(request, response):
        return response.render("/wifi", **{
            "SSID_SELECTOR": WifiSelector(*[network["ssid"] for network in Wifi.networks]), # todo: WLAN netwerk scan => Arg parse erin
            "MESSAGE": "Failed to connect to wifi, please connect to a nearby access point"
        })

    @WebserverRoute.post("/wifi")
    def wifi_post(request, response):
        params = request.PARAMS
        message = """
            <b>Attempting to connect to {ssid}.. page will reload in a second.</b>
            {redirect}
        """.format(ssid=" ".join(params["ssid"].split("+")), redirect=Redirect("/", 5000))
        
        if not len(request.PARAMS):
            message = "Wifi not connected, please connect to a wifi access point."
        elif not all(i in params.keys() for i in ["ssid", "password"]):
            message = "Wifi SSID or password was not set"
        
        return response.render("/wifi", **{
            "SSID_SELECTOR": WifiSelector(*[network["ssid"] for network in Wifi.networks]), # todo: WLAN netwerk scan => Arg parse erin
            "MESSAGE": message
        })

    @WebserverRoute.get("/change_adhoc")
    def adhoc_set_get(request, response):
        return response.render("/change_adhoc", **{
            "MESSAGE": "Failed to connect to wifi, please connect to a nearby access point"
        })

    @WebserverRoute.post("/change_adhoc")
    def adhoc_set_post(request, response):
        params = request.PARAMS

        message = "<b>Assigning new access point password.</b>"
        if not len(request.PARAMS) or not all(i in params.keys() for i in ["password", "password_verify"]):
            message = "Invalid request"
        elif params["password"] != params["password_verify"]:
            message = "Passwords did not match"

        return response.render("/change_adhoc", **{
            "MESSAGE": message
        })
