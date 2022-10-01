from os import listdir
import socket
import re

from WebserverRequest import WebserverRequest
from WebserverResponse import WebserverResponse
from Pages import Pages # Laten staan, is nodig om de webpaginas in te laden.


class Webserver:
    """
        Internal webserver, used for updating wifi connection and presenting QR code to end user to link device to main server.
    """

    # Socket config
    __socket = None
    __ADDR = 0
    __RECEIVE_BUFFER_SIZE = pow(2, 10)

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

            try: 
                request = WebserverRequest.parse(client_request.decode("utf-8"))
            except Exception as e: 
                print(e)
                request = WebserverRequest.status_503(e)
            finally:
                response = WebserverResponse(client, request)
                request.SendResponse(response)
                
                # client.send(bytes('HTTP/1.0 {STATUS} OK\r\nContent-type: text/html\r\n\r\n{RESPONSE}'.format(STATUS=request.STATUS_CODE, RESPONSE=requestParser(params)), "utf-8"))

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
