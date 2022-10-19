
import re
from components.layout.Header import Header
from net.www.mime.MimeBaseTypes import MimeBaseTypes
from net.www.mime.MimeTypes import MimeTypes

from utils.Path import file_exists
from net.www.WebserverRoute import WebserverRoute
from utils.Device import Device
from net.www.HTTPHeader import HTTPHeader
from net.www.HTTPResponse import HTTPResponse

from Routes import Routes

"""
#!TODO: Check images and other binary request, currently is send "improperly".

"""
class HTTPRequest(HTTPHeader):
    __PUBLIC_FOLDER = "public"
    __response = None
    
    def __init__(self, request_header):
        super().__init__(request_header)
        
    @property
    def response(self):
        if self.__response is None:
            self.__response = self.__buildResponse()
            
        return self.__response
        
    def __buildResponse(self):
        response = HTTPResponse(self)
        route_parser = WebserverRoute.fetch(self.http_method, self.absolute_path)
        
        if route_parser:
            response.data = route_parser(self, response)
        else:
            file_ext = self.file_extension
            if file_ext is None or (file_ext is not None and not file_exists(f"/{self.__PUBLIC_FOLDER}{self.absolute_path}")):
                response.status_code = 404
                response.content_type = "text/html"
                response.data = "Page not found"
            
            if response.status_code == 200:
                response.data = response.getPublicFile()
        
        return response
            
         
if __name__ == "__main__":
    request = HTTPRequest("""GET /wifi?hello=1=a&yello=d HTTP/1.1
    Host: 192.168.1.54
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
    Accept-Language: nl,en-US;q=0.7,en;q=0.3
    Accept-Encoding: gzip, deflate
    Referer: http://192.168.1.54/
    Connection: keep-alive
    Upgrade-Insecure-Requests: 1
    DNT: 1
    Sec-GPC: 1\r\n\r\n
    hello=2&yello=a""")
    
    response = request.response

    print(f"{type(response.data)} => {response.data}") 
    

