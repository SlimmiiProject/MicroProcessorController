from os import listdir
import socket
import re

from numpy import mat


class Pages:
    @staticmethod 
    def __readEndpointFile(name): 
        file = open("{ROOT}/{NAME}.html".format(ROOT="./endpoints", NAME=name), "r")
        page = "".join(file.readlines())

        return page

    @staticmethod
    def __parseParameters(page, params):
        match = re.search(r"\{(.*?)\}", page)

        while True:
            match =  re.search(r"\{(.*?)\}", page)
            if match is None :
                break

            match = match.group()
            key = str(match)[1:-1]
            page = page.replace(match, params[key])
             
        return page
        
    @staticmethod
    def index(params):
        return Pages.__readEndpointFile("index")

    @staticmethod
    def wifi(params):
        if len(params) == 0 :
            params["MESSAGE"] = ""
        elif not all(i in params.keys() for i in ["ssid", "password"]):
            params["MESSAGE"] = "Wifi SSID or password was not set"
        else:
            params["MESSAGE"] = "Wifi succesfully set."
        
            
        return  Pages.__parseParameters(Pages.__readEndpointFile("wifi"), params)

    @staticmethod
    def status_404(params):
        return "Page not found"

    @staticmethod
    def status_503(params):
        return "<b>Server error:</b> {error}".format(error=params["error"])

class Webserver:
    """
        Internal webserver, used for updating wifi connection and presenting QR code to end user to link device to main server.
    """

    # Socket config
    __socket = None
    __ADDR = 0
    __RECEIVE_BUFFER_SIZE = pow(2, 10)

    # Endpoint config
    __ENDPOINTS = []
    __CUSTOM_PARSER = {}

    def __init__(self,  endpoints="./endpoints", port = 8080, maxClients = 1) -> None:
        
        # Fetch none-reroute addr info en stel de readonly max client in.
        self.__ADDR = socket.getaddrinfo("0.0.0.0", port)[0][-1]
        self.__MAX_CLIENTS = maxClients

        # Creer socket object, bind op none-rerout (Niet op loopback address binden (127.0.0.1) dit is intern dus server niet toegankelijk)
        self.__socket = socket.socket()
        self.__socket.bind(self.__ADDR)
        
        # Laad endpoint namen MAAR NIET DATA! 4MB RAM!


    def __handleRequest(self):
        """
            Handle an incomming client request, and present 404 or page content.
        """
        client = None
        try:
            client, addr = self.__socket.accept()
            print("Client connected from: {client_addr}".format(client_addr=addr))
            client_request = client.recv(self.__RECEIVE_BUFFER_SIZE)

            status_code = -1
            request = Pages.status_503
            try: 
                # Split HTTP request, fetch GET lijn, Split lijn en fetch 2de index (1) (GET /ENDPOINT HTTP1.0)
                requestType, endpoint, _ = list(filter(lambda i: "GET" in i, client_request.decode("utf-8").split("\n")))[0].split(" ")
                endpoint = endpoint[1:] if len(endpoint) > 1 else "index" # Strip leading backslash (/)
                params = {}
                if "?" in endpoint:
                    params = dict([ i.split("=") for i in endpoint.split("?")[-1].split("&")])
                    endpoint = endpoint.split("?")[0]

            except Exception as e: 
                status_code = 504
                params = {"error": str(e)}
            finally:
                if status_code < 0: 
                    status_code = 200 if endpoint in Pages.__dict__.keys() else 404
                    request = Pages.__dict__[endpoint] if status_code == 200 else Pages.status_404

            client.send(bytes('HTTP/1.0 {STATUS} OK\r\nContent-type: text/html\r\n\r\n{RESPONSE}'.format(STATUS=status_code, RESPONSE=request(params)), "utf-8"))
        except OSError as e:
            print("Failed loading endpoint")
        finally:
            if client is not None:
                client.close()

    def start(self): 
        """
            Start server and wait for incomming client requests.
        """
        # Start socket en wacht op inkomende connectie requests.
        self.__socket.listen(self.__MAX_CLIENTS)

        # Moet async worden met asyncio of alternatief gebaseerd op micropython
        while True:
            self.__handleRequest()

# Test functie, werkt enkel indien je de file direct in de python interpeter inlaad.
if __name__ == "__main__": 
    Webserver().start()
