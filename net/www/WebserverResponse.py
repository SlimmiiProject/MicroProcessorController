from re import search

from net.www.mime.MimeBaseTypes import MimeBaseTypes
from net.www.mime.MimeTypes import MimeTypes


class WebserverResponse: 
    __client = None

    http_version = "HTTP/1.1"
    status_code = 200
    content_type = "text/html"

    def __init__(self, client) -> None:
        self.__client = client

    def send(self, data):   
        header = '{VERSION} {STATUS} OK\r\nContent-type: {CONTENT_TYPE}\r\n\r\n'.format(VERSION=self.http_version,STATUS=self.status_code, CONTENT_TYPE=self.content_type)
        data = bytes(data, "utf-8") if isinstance(data, str) else data

        if data is not None:
            self.__client.send(bytes(header, "utf-8"))
            self.__client.send(data)
         
    def render(self, endpoint, **kwargs):     
        html = self.__parseParameters(self.sendFile(endpoint[1:]+".html", MimeTypes[".html"]), **kwargs)
        return self.send(html)
    
    def sendFile(self, endpoint, content_type):
        self.content_type, file_ext = [content_type, "."+endpoint.split(".")[-1]]
   
        if file_ext in MimeBaseTypes[str]:
            content = self.__readTextFile(endpoint)
        elif file_ext in MimeBaseTypes[bytes]:
            content = self.__readBinaryFile(endpoint[1:])
        
        return self.send(content)

    @staticmethod 
    def __readTextFile(endpoint): 
        file = open("{ROOT}/{NAME}".format(ROOT="./routes", NAME=endpoint), "r")
        page = "".join(file.readlines())
        file.close()

        return page
    @staticmethod 
    def __readBinaryFile(endpoint): 
        file = open("{ROOT}/{NAME}".format(ROOT="./routes", NAME=endpoint), "rb")
        binary = file.read()
        file.close()

        return binary

    @staticmethod
    def __parseParameters(html, **kwargs):
        while html is not None: 
            # Zoek {KEY_NAAM} in de pagina broncode. 
            match =  search(r"\{(.*?)\}", html)
            if match is None:
                break

            # Parse match en key voor parameter hashmap.
            match = match.group()
            key = str(match)[1:-1]
            
            html = html.replace(match, kwargs[key])
             
        return html
        