
import re
from net.www.mime.MimeBaseTypes import MimeBaseTypes
from net.www.mime.MimeTypes import MimeTypes

from net.www.WebserverRoute import WebserverRoute

class WebserverRequest:
    __REQUEST_DATA = {
        "REQUEST_METHOD": None,
        "ENDPOINT": None,
        "PARAMS": None,
        "CALLBACK": None,
        "RESPONSE": None
    }

    def __init__(self, **kwargs) -> None:
        assert all([key in kwargs.keys() for key in self.__REQUEST_DATA.keys()])
        self.__REQUEST_DATA = kwargs
    
    def __getKey(self, key): 
        """
            Fetch a request data object from local request data dictionary
        """
        return self.__REQUEST_DATA[key]

    def sendResponse(self):
        """
            Execute request parser callback with response as parameter
        """
        return self.__getKey("CALLBACK")(self, self.__getKey("RESPONSE"))

    @staticmethod
    def __parseParams(method, endpoint, request_header): 
        """
            Parse HTTP parameters from request header (Probably will remove this function for a parse string instead, to much unecessary params)
        """
        def parseSet(input_str):
            return dict([(param.split("=") if "=" in param else [param, True]) for param in input_str.split("?")[1].split("&")]) if "?" in input_str else {}
            
        params = parseSet(endpoint)
        if method.upper() == "POST":
            params = {**params, **parseSet("?"+request_header.split("\n")[-1])}

        return params
    
    #region properties
    @property
    def REQUEST_METHOD(self):
        """
            HTTP Request method
        """
        return self.__getKey("REQUEST_METHOD")

    @property
    def ENDPOINT(self):
        """
            HTTP Endpoint
        """
        return self.__getKey("ENDPOINT")

    @property
    def PARAMS(self):
        """
            HTTP browser parameters
        """
        return self.__getKey("PARAMS")
    #endregion

    #region classmethods
    @classmethod
    def parse(cls, response, request_header) -> None:
        """
            Parse HTTP Request header to WebserverRequest
        """
        
        # Zoek achter de request method & endpoint met regex 
        method, endpoint = re.search(r"^[a-zA-Z]{3,7} \/[\S]*", request_header).group().split(" ")
        endpoint, abs_path = [
            endpoint if endpoint != "/index" else "/", 
            endpoint.split("?")[0] if "?" in endpoint else endpoint
        ]
        
        # Parse object als file request.
        if "." in abs_path:
            file_ext = "."+abs_path.split(".")[-1]
            print( MimeBaseTypes.values())
            print(any([file_ext in set for set in MimeBaseTypes.values()]))
            if any([file_ext in set for set in MimeBaseTypes.values()]):
                return WebserverRequest.__sendFile(abs_path, response)

        # Parse HTML
        requestParser = WebserverRoute.fetch(method, abs_path)
        if not requestParser:
            return WebserverRequest.status_404(response)

        params = WebserverRequest.__parseParams(method, endpoint, request_header)
        return cls(**{
            "REQUEST_METHOD": method,
            "ENDPOINT": endpoint,
            "PARAMS": params,
            "CALLBACK": requestParser,
            "RESPONSE": response
        });
    
    @classmethod
    def __sendFile(cls, endpoint, server_response):
        def send(request, response):
            return response.sendFile(endpoint, MimeTypes["."+endpoint.split(".")[-1]])

        return cls(**{
            "REQUEST_METHOD": "GET",
            "ENDPOINT": endpoint,
            "PARAMS": {},
            "CALLBACK": send,
            "RESPONSE": server_response
        });

    @classmethod
    def status_404(cls, server_response):
        """
            Class constructor for 404 status WebserverRequest object
        """
        def responseCallback(request, response):
            return response.send("<h1>Page not found</h1>")
        server_response.status_code = 404

        kwargs = WebserverRequest.__REQUEST_DATA
        kwargs["CALLBACK"] = responseCallback
        kwargs["RESPONSE"] = server_response

        return cls(**kwargs)

    @classmethod
    def status_503(cls, server_response, error = None):
        """ 
            Class constructor for 503 status WebserverRequest object
        """
        def responseCallback(request, response):
            return response.send("<h1>Internal server error:</h1>{e}".format(e=error))

        server_response.status_code = 503

        kwargs = WebserverRequest.__REQUEST_DATA
        kwargs["CALLBACK"] = responseCallback
        kwargs["RESPONSE"] = server_response

        return cls(**kwargs)
    #endregion
