from re import search

class WebserverResponse: 
    __client = None
    __request = None

    def __init__(self, client, request) -> None:
        self.__client = client
        self.__request = request

    def send(self, html):                
        return self.__client.send(bytes('HTTP/1.0 {STATUS} OK\r\nContent-type: text/html\r\n\r\n{RESPONSE}'.format(STATUS=self.__request.STATUS_CODE, RESPONSE=html), "utf-8"))
         
    def render(self, endpoint, **kwargs):                
        html = self.__parseParameters(self.__readEndpointFile(endpoint[1:]), **kwargs)
        return self.__client.send(bytes('HTTP/1.0 {STATUS} OK\r\nContent-type: text/html\r\n\r\n{RESPONSE}'.format(STATUS=self.__request.STATUS_CODE, RESPONSE=html), "utf-8"))
         
    @staticmethod 
    def __readEndpointFile(endpoint): 
        file = open("{ROOT}/{NAME}.html".format(ROOT="./routes", NAME=endpoint), "r")
        page = "".join(file.readlines())

        return page

    @staticmethod
    def __parseParameters(html, **kwargs):
        while True: 
            # Zoek {KEY_NAAM} in de pagina broncode. 
            match =  search(r"\{(.*?)\}", html)
            if match is None:
                break

            # Parse match en key voor parameter hashmap.
            match = match.group()
            key = str(match)[1:-1]
            
            html = html.replace(match, kwargs[key])
             
        return html
        