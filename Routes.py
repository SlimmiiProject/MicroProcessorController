 
from re import search as searchPattern
from components.WifiSelector import WifiSelector

from net.www.WebserverRoute import WebserverRoute



class Routes:
    @staticmethod 
    def __readEndpointFile(name): 
        file = open("{ROOT}/{NAME}.html".format(ROOT="./routes", NAME=name), "r")
        page = "".join(file.readlines())

        return page

    @staticmethod
    def __parseParameters(page, params):
        while True: 
            # Zoek {KEY_NAAM} in de pagina broncode. 
            match =  searchPattern(r"\{(.*?)\}", page)
            if match is None :
                break

            # Parse match en key voor parameter hashmap.
            match = match.group()
            key = str(match)[1:-1]
            
            page = page.replace(match, params[key])
             
        return page
        
    @WebserverRoute.get("/")
    def index(request, response):
        return response.send(Routes.__readEndpointFile("index"))

    @WebserverRoute.get("/wifi")
    def wifi(request, response):
        params = request.PARAMS
        params["SSID_SELECTOR"] = WifiSelector("hello world")
        if len(request.PARAMS) == 0 :
            params["MESSAGE"] = "Wifi not connected, please connect to a wifi access point."
        elif not all(i in params.keys() for i in ["ssid", "password"]):
            params["MESSAGE"] = "Wifi SSID or password was not set"
        else:
            params["MESSAGE"] = "Wifi succesfully set."
        
        return response.send(Routes.__parseParameters(Routes.__readEndpointFile("wifi"), params))

    @WebserverRoute.post("/wifi")
    def wifi(request, response):
        params = request.PARAMS
        params["SSID_SELECTOR"] = WifiSelector("hello posted world")
        if not len(request.PARAMS) :
            params["MESSAGE"] = "Wifi not connected, please connect to a wifi access point."
        elif not all(i in params.keys() for i in ["ssid", "password"]):
            params["MESSAGE"] = "Wifi SSID or password was not set"
        else:
            params["MESSAGE"] = "Wifi succesfully set."
        
        return response.send(Routes.__parseParameters(Routes.__readEndpointFile("wifi"), params))
