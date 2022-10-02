class WebserverResponse: 
    __client = None
    __request = None

    def __init__(self, client, request) -> None:
        self.__client = client
        self.__request = request

    def send(self, html):                
        return self.__client.send(bytes('HTTP/1.0 {STATUS} OK\r\nContent-type: text/html\r\n\r\n{RESPONSE}'.format(STATUS=self.__request.STATUS_CODE, RESPONSE=html), "utf-8"))
         
    def render(self, **kwargs):                
        
        return self.__client.send(bytes('HTTP/1.0 {STATUS} OK\r\nContent-type: text/html\r\n\r\n{RESPONSE}'.format(STATUS=self.__request.STATUS_CODE, RESPONSE=html), "utf-8"))
         