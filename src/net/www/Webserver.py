from os import listdir
import socket
import re

from Routes import Routes # Laten staan, is nodig om de webpaginas in te laden.
from net.www.WebserverResponse import WebserverResponse 
from net.www.WebserverRequest import WebserverRequest 


class Webserver:
    """
        Internal webserver, used for updating wifi connection and presenting QR code to end user to link device to main server.
    """

    # Socket config
    __RECEIVE_BUFFER_SIZE = pow(2, 10)

    def __init__(self,  port = 8080, maxClients = 1) -> None:
        """
            Initialize socket and private properties.
        """
        # Fetch none-reroute addr info en stel de readonly max client in.
        self.__ADDR = socket.getaddrinfo("0.0.0.0", port)[0][-1]
        self.__MAX_CLIENTS = maxClients

        # Creer socket object, bind op none-rerout (Niet op loopback address binden (127.0.0.1) dit is intern dus server niet toegankelijk)
        self.__socket = socket.socket()
        self.__socket.bind(self.__ADDR)
        


    def __handleRequest(self):
        """
            Handle an incomming client request, and present 404 or page content.
        """

        client = None
            
        try:
            client, addr = self.__socket.accept()
            print("Client connected from: {client_addr}".format(client_addr=addr))
            client_request = client.recv(self.__RECEIVE_BUFFER_SIZE)
            
            response = WebserverResponse(client)
            request = WebserverRequest.parse(response, client_request.decode("utf-8"))
            request.sendResponse()
            try:
                pass
            except Exception as e:
                print("error")
                print(e)
        except OSError as e:
            print("Failed loading endpoint")
            print(e)
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
