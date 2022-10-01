 
from re import search as searchPattern
from Route import Route


class Pages:
    @staticmethod 
    def __readEndpointFile(name): 
        file = open("{ROOT}/{NAME}.html".format(ROOT="./endpoints", NAME=name), "r")
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
        
    @Route.get("/")
    def index(request, response):
        return response.send(Pages.__readEndpointFile("index"))

    @Route.get("/wifi")
    def wifi(request, response):
        params = request.PARAMS
        if len(request.PARAMS) == 0 :
            params["MESSAGE"] = ""
        elif not all(i in params.keys() for i in ["ssid", "password"]):
            params["MESSAGE"] = "Wifi SSID or password was not set"
        else:
            params["MESSAGE"] = "Wifi succesfully set."
        
        return response.send(Pages.__parseParameters(Pages.__readEndpointFile("wifi"), params))
