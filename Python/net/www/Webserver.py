from os import listdir
import socket
import re
import uasyncio

from net.www.HTTPRequest import HTTPRequest 
from net.www.HTTPResponse import HTTPResponse
from utils.Logger import Logger

from net.Wifi import Wifi


class Webserver:
    """
        Internal webserver, used for updating wifi connection and presenting QR code to end user to link device to main server.
    """

    # Socket config
    __RECEIVE_BUFFER_SIZE = pow(2, 10)

    def __init__(self, ip=Wifi.adhoc_ip_adress, port = 80, maxClients = 1) -> None:
        """
            Initialize socket and private properties.
        """
        # Fetch none-reroute addr info en stel de readonly max client in.
        self.__ADDR = socket.getaddrinfo("0.0.0.0" if ip is None else ip, port)[0][-1]
        self.__MAX_CLIENTS = maxClients

        # Creer socket object, bind op none-rerout (Niet op loopback address binden (127.0.0.1) dit is intern dus server niet toegankelijk)
        self.__socket = socket.socket()
        self.__socket.bind(self.__ADDR)
        self.__socket.setblocking(False)
        self.__socket.listen(self.__MAX_CLIENTS)


    def __handleRequest(self):
        """
            Handle any incomming client request
        """

        client = None
            
        try:
            client, addr = self.__socket.accept()
            client.setblocking(True)
            
            client_request = client.recv(self.__RECEIVE_BUFFER_SIZE).decode("utf-8")
            http_request = HTTPRequest(client_request)
            Logger.log(self, f"Client connected from: {addr[0]} requesting path: {http_request.endpoint}")
            response = http_request.response
            
            http_request.response.send(client)
        except Exception as e:
            if not e.errno == 11:
                raise (e)
        except ValueError as e:
            print(e)
        finally:
            if client is not None:
                client.close()

    async def start(self): 
        """
            Start server and wait for incomming client requests.
        """
        # Start socket en wacht op inkomende connectie requests.
        # Moet async worden met asyncio of alternatief gebaseerd op micropython
        while True:
            self.__handleRequest()
            
            await uasyncio.sleep_ms(100)