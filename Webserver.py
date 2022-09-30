from os import listdir
import socket

class Webserver:
    """
    Webserver die zal gebruikt worden voor het connecteren met de wifi & QR voor connectie zal displayen.
    """
    
    # Socket config
    __socket = None
    __ADDR = 0
    __RECEIVE_BUFFER_SIZE = pow(2, 10)

    # Endpoint config
    __ENDPOINT_ROOT = "./endpoints"
    __ENDPOINTS = []

    def __init__(self, port = 8080, maxClients = 1) -> None:
        # Fetch none-reroute addr info en stel de readonly max client in.
        self.__ADDR = socket.getaddrinfo("0.0.0.0", port)[0][-1]
        self.__MAX_CLIENTS = maxClients

        # Creer socket object, bind op none-rerout (Niet op loopback address binden (127.0.0.1) dit is intern dus server niet toegankelijk)
        self.__socket = socket.socket()
        self.__socket.bind(self.__ADDR)
        
        # Laad endpoint namen MAAR NIET DATA! 4MB RAM!
        self.__setupEndpoints()


    def __setupEndpoints(self): 
        # Laad endpoints in en push op de endpoint stack.
        for filename in listdir(self.__ENDPOINT_ROOT):
            self.__ENDPOINTS.append(filename.split(".html")[0])

        print(self.__ENDPOINTS)


    def start(self): 
        # Start socket en wacht op inkomende connectie requests.
        self.__socket.listen(self.__MAX_CLIENTS)

        # Moet async worden met asyncio of alternatief gebaseerd op micropython
        while True:
            self.handleRequest()

    def handleRequest(self):
        client = None
        try:
            client, addr = self.__socket.accept()
            print("Client connected from: {client_addr}".format(client_addr=addr))
            client_request = client.recv(self.__RECEIVE_BUFFER_SIZE)

            # Split HTTP request, fetch GET lijn, Split lijn en fetch 2de index (1) (GET /ENDPOINT HTTP1.0)
            requestType, endpoint, _ = list(filter(lambda i: "GET" in i, client_request.decode("utf-8").split("\n")))[0].split(" ")
            endpoint = endpoint[1:] if len(endpoint) > 1 else "index" # Strip leading backslash (/)

            # Stel status code in op 200 (tijdelijk betere handling hiervoor nodig) indien endpoint gevonden anders 404 (mogelijk nog 404 opmaken en filteren uit mogelijke endpoints met numreg)
            status = 200 if endpoint in self.__ENDPOINTS else 404
            page = "Failed to load page"
            if status == 200:
                file = open("{ROOT}/{NAME}.html".format(ROOT=self.__ENDPOINT_ROOT, NAME=endpoint), "r")
                page = "".join(file.readlines())

            client.send(bytes('HTTP/1.0 {STATUS} OK\r\nContent-type: text/html\r\n\r\n{RESPONSE}'.format(STATUS=status, RESPONSE=page), "utf-8"))
        except FileExistsError as e:
            print(e)
        finally:
            if client is not None:
                client.close()

    
# Test functie, werkt enkel indien je de file direct in de python interpeter inlaad.
if __name__ == "__main__": 
    Webserver().start()
