
import re

from WebserverRoute import WebserverRoute


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
        return self.__REQUEST_DATA[key]

    @property
    def REQUEST_METHOD(self):
        return self.__getKey("REQUEST_METHOD")

    @property
    def ENDPOINT(self):
        return self.__getKey("ENDPOINT")

    @property
    def PARAMS(self):
        return self.__getKey("PARAMS")

    @property
    def STATUS_CODE(self):
        return self.__getKey("STATUS_CODE")

    def SendResponse(self, response):
        return self.__getKey("CALLBACK")(self, response)
    
    @classmethod
    def parse(cls, requestStr) -> None:
        # Zoek achter de request method & endpoint met regex 
        method, endpoint = re.search(r"^[a-zA-Z]{3,7} \/[\S]*", requestStr).group().split(" ")
        endpoint = endpoint if endpoint != "/index" else "/"

        requestParser = WebserverRoute.fetch(method, endpoint)
        if not requestParser:
            print("Page not found sending 404")
            return WebserverRequest.status_404()

        params = dict([(param.split("=") if "=" in param else [param, True]) for param in endpoint.split("?")[1].split("&")]) if "?" in endpoint else {}

        return cls(**{
            "REQUEST_METHOD": method,
            "ENDPOINT": endpoint,
            "PARAMS": params,
            "CALLBACK": requestParser,
            "STATUS_CODE": 200
        });

    @classmethod
    def status_404(cls):
        def responseCallback(request, response):
            return response.send("<h1>Page not found</h1>")

        kwargs = WebserverRequest.__REQUEST_DATA
        kwargs["STATUS_CODE"] = 404
        kwargs["CALLBACK"] = responseCallback

        return cls(**kwargs)

    @classmethod
    def status_503(cls, error = None):
        def responseCallback(request, response):
            return response.send("<h1>Internal server error:</h1>{e}".format(e=error))

        kwargs = WebserverRequest.__REQUEST_DATA
        kwargs["STATUS_CODE"] = 504
        kwargs["CALLBACK"] = responseCallback

        return cls(**kwargs)