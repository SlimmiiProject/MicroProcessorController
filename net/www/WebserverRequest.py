
import re

from net.www.WebserverRoute import WebserverRoute

class WebserverRequest:
    __REQUEST_DATA = {
        "REQUEST_METHOD": None,
        "ENDPOINT": None,
        "PARAMS": None,
        "CALLBACK": None,
        "STATUS_CODE": None
    }

    def __init__(self, **kwargs) -> None:
        assert all([key in kwargs.keys() for key in self.__REQUEST_DATA.keys()])
        self.__REQUEST_DATA = kwargs
    
    def __getKey(self, key): 
        """
            Fetch a request data object from local request data dictionary
        """
        return self.__REQUEST_DATA[key]

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

    @property
    def STATUS_CODE(self):
        """
            HTTP status code
        """
        return self.__getKey("STATUS_CODE")

    def sendResponse(self, response):
        """
            Execute request parser callback with response as parameter
        """
        return self.__getKey("CALLBACK")(self, response)
    
    @classmethod
    def parse(cls, requestStr) -> None:
        """
            Parse HTTP Request header to WebserverRequest
        """
        # Zoek achter de request method & endpoint met regex 
        method, endpoint = re.search(r"^[a-zA-Z]{3,7} \/[\S]*", requestStr).group().split(" ")
        endpoint, abs_path = [endpoint if endpoint != "/index" else "/", endpoint.split("?")[0] if "?" in endpoint else endpoint]

        requestParser = WebserverRoute.fetch(method, abs_path)
        if not requestParser:
            return WebserverRequest.status_404()

        params = WebserverRequest.__parseParams(method, endpoint, requestStr)
        return cls(**{
            "REQUEST_METHOD": method,
            "ENDPOINT": endpoint,
            "PARAMS": params,
            "CALLBACK": requestParser,
            "STATUS_CODE": 200
        });

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

    @classmethod
    def status_404(cls):
        """
            Class constructor for 404 status WebserverRequest object
        """
        def responseCallback(request, response):
            return response.send("<h1>Page not found</h1>")

        kwargs = WebserverRequest.__REQUEST_DATA
        kwargs["STATUS_CODE"] = 404
        kwargs["CALLBACK"] = responseCallback

        return cls(**kwargs)

    @classmethod
    def status_503(cls, error = None):
        """ 
            Class constructor for 503 status WebserverRequest object
        """
        def responseCallback(request, response):
            return response.send("<h1>Internal server error:</h1>{e}".format(e=error))

        kwargs = WebserverRequest.__REQUEST_DATA
        kwargs["STATUS_CODE"] = 503
        kwargs["CALLBACK"] = responseCallback

        return cls(**kwargs)
