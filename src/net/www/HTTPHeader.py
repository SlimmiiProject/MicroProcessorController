import re
from net.www.mime.MimeTypes import MimeTypes

class HTTPHeader:
    
    __response_order = ["Date", "Expires", "Cache-Control", "Content-Type", "Server", "X-XSS-Protection", "X-Frame-Options", "Set-Cookie", "Accept-Ranges", "Vary", "Transfer-Encoding"]
    __key_order = ["Host", "Content-Type", "User-Agent", "Accept-Language", "Accept-Encoding", "Referer", "Connection", "DNT", "Sec-GPC"]
    __allowed_keys = {"Host", "User-Agent", "Accept-Language", "Accept-Encoding", "Referer", "Connection", "DNT", "Sec-GPC", "Version", "Content-Type", "Code", "Data", "Params"}
    
    def __init__(self, request_string):
        self.__parse(request_string)
        
    #region Properties
    @property
    def host(self):
        """
            HTTP_HEADER => Host
            
            The domain name of the server.
        """
        return self.__getKey("Host")
    
    @host.setter
    def host(self, value):
        return self.__setKey("Host", value)
    
    @property
    def user_agent(self):
        """
            HTTP_HEADER => User-Agent
            
            Identifier for the operating system, vendor and/or version.
        """
        return self.__getKey("User-Agent")
    
    @user_agent.setter
    def user_agent(self, value):
        return self.__setKey("User-Agent", value)
    
    @property
    def accept(self):
        """
            HTTP_HEADER => Accept
            
            A represantation of the MIME types a client is able to understand. 
        """
        return self.__getKey("Accept")
    
    @accept.setter
    def accept(self, value):
        return self.__setKey("Accept", value)
    
    @property
    def date(self):
        """
            HTTP_HEADER => Date
            
            A representation of the time the request was send of one endpoint (request or response) 
        """
        return self.__getKey("Date")
    
    @date.setter
    def date(self, value):
        return self.__setKey("Date", value)
    
    @property
    def transfer_encoding(self):
        """
            HTTP_HEADER => Transfer-Encoding
            
            Specifies the form of encoding used to safely transfer the data payload to the client.
        """
        return self.__getKey("Transfer-Encoding")
     
    @transfer_encoding.setter
    def transfer_encoding(self, value):
        return self.__setKey("Transfer-Encoding", value)
    
    @property
    def connection(self):
        """
            HTTP_HEADER => Connection
            
            Represent the state of the connection to uphold. 
        """
        return self.__getKey("Connection")
    
    @connection.setter
    def connection(self, value):
        return self.__setKey("Connection", value)
    
    @property
    def cache_control(self):
        """
            HTTP_HEADER => Cache-Control
            
            Represents the instructions for both requests and responses that controls browser caching.
        """
        return self.__getKey("Cache-Control")
    
    @cache_control.setter
    def cache_control(self, value):
        return self.__setKey("Cache-Control", value)
    
    @property
    def expires(self):
        """
            HTTP_HEADER => Expires
            
            Represent the data/time when the payload will be expired. 
        """
        return self.__getKey("Expires")
     
    @expires.setter
    def expires(self, value):
        return self.__setKey("Expires", value)
    
    @property
    def location(self):
        """
            HTTP_HEADER => Location
            
            Indicated the url to redirect a page to. (only should be used in 3xx or 201 (created) status response) 
        """
        return self.__getKey("Location")
    
    @location.setter
    def location(self, value):
        return self.__setKey("Location", value)
    
    @property
    def http_method(self):
        """
            HTTP_HEADER => {Method} {Endpoint} {Version}
            
            The method a request is made or should be uphold to. First line of header no key specified for this argument. 
        """
        return self.__getKey("Method")
    
    @http_method.setter
    def http_method(self, value):
        return self.__setKey("Method", value)
    
    @property
    def absolute_path(self):
        """
            Internal_Property => Absolute-Path
            
            A representation of the endpoint stripped of parameter data.
        """
        return self.__getKey("Absolute-Path")
       
    @absolute_path.setter
    def absolute_path(self, value):
        return self.__setKey("Absolute-Path", value)
     
    @property
    def endpoint(self):
        """
            HTTP_HEADER => {Method} {Endpoint} {Version}
            
            The server endpoint requested by the client.
        """
        return self.__getKey("Endpoint")
    
    @endpoint.setter
    def endpoint(self, value):
        return self.__setKey("Endpoint", value)
    
    @property
    def content_type(self):
        """
            HTTP_HEADER => Content-Type
            
            The MIME type of the content that will be send as data.
        """
        return self.__getKey("Content-Type")
    
    @content_type.setter
    def content_type(self, value):
        return self.__setKey("Content-Type", value)
    
    @property
    def status_code(self):
        """
            
        """
        return self.__getKey("Code")
    
    @status_code.setter
    def status_code(self, value):
        return self.__setKey("Code", value)
    
    @property
    def version(self):
        return self.__getKey("Version")
    
    @version.setter
    def version(self, value):
        return self.__setKey("Version", value)
    
    @property
    def data(self):
        return self.__getKey("Data")
    
    @data.setter
    def data(self, value):
        return self.__setKey("Data", value)
    
    @property
    def __request_header_input(self):
        return self.__getKey("Raw")
    
    @property
    def parameters(self):
        return self.__getKey("Params")
    
    @property
    def file_extension(self):
        file_ext = self.absolute_path[self.absolute_path.find(".")+1:] if "." in self.absolute_path else None 
        return None if file_ext is None else (file_ext if len(file_ext) > 0 else None)
    #endregion
    
    
    #region Functions
    def __parse(self, request_header):
        
        request_header_lines = request_header.split("\n") if isinstance(request_header, str) else []
        if len(request_header_lines) == 0 or len(request_header_lines[0].split(" ")) != 3:
            method, endpoint, abs_path = ["GET", "/", "/"]
        else:
            method, endpoint, _ = request_header_lines[0].split(" ")
            endpoint, abs_path = [
                endpoint if endpoint != "/index" else "/", 
                endpoint.split("?")[0] if "?" in endpoint else endpoint
            ]
        
        self.__config = {
             "Version": "HTTP/1.1",
             "Code": 200,
             "Content-Type":"text/html",
             "Data": "",
             "Params": {},
             "Raw": request_header
        }
        
        self.__config.update({k.strip(): v.strip() for k, v in list(map(lambda line: [line[0:(line.find(": "))], line[line.find(": ")+2:len(line)]],request_header_lines[1:]))})
        self.__config.update({
             "Method": method,
             "Endpoint": endpoint, 
             "Absolute-Path": abs_path 
        })
        
        if self.file_extension is not None:
            self.content_type = MimeTypes[f".{self.file_extension}"]
        else:
            self.content_type = "text/plain"
        
        self.__parseParameters()
        
    
    def __parseParameters(self):
        """
            Parse http_header endpoint and body parameters. 
        """
        def parse_line(source, line):
            entries = dict(map(lambda i: [i[0:i.find("=")], i[i.find("=")+1:len(i)]] if "=" in i else [i, True], line.split("&")))
            return {k:v for d in [source, entries] for k,v in d.items()}

        param_set = {}
        # Parse URI before body for GET attacks
        if "?" in self.endpoint:
            param_set = parse_line(param_set, self.endpoint[self.endpoint.find("?")+1:len(self.endpoint)])
        
        if len(self.__request_header_input.split("\r\n\r\n"))  > 1:
            param_set = parse_line(param_set, self.__request_header_input[self.__request_header_input.find("\r\n\r\n"):].strip())
        
        self.__config["Params"] = param_set
          
    def __getKey(self, key):
    
        assert key in self.__config.keys()
        
        return self.__config[key]
    
    def __setKey(self, **kwargs):
        for key, value in kwargs.items():
            self.__setKey(key, value)
       
       
    def __setKey(self, key, value):
        self.__config[key] = value
    
    def setParams(self, **kwargs):
        return self.__setKey("Params", {k:v for d in [self.parameters, kwargs] for k,v in d.items()} )
    
    def toString(self, request_type = 0):
        conf_keys = self.__config.keys()
        request_header = f"{self.http_method} {self.endpoint} {self.status_code}\r\n" if request_type == 0 else f"{self.version} {self.status_code}\r\n"
        
        for key in [self.__key_order, self.__response_order][request_type]:
            if key in conf_keys:
                request_header += f"{key}: {self.__config[key]}\r\n"
        
        request_header += "\r\n\r\n" 
        
        return request_header
    #endregion
    
if __name__ == "__main__":
    request = HTTPHeader("""GET /wifi.txt?hello=1=a&yello=d HTTP/1.1\nHost: 192.168.1.54\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: nl,en-US;q=0.7,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: http://192.168.1.54/
Connection: keep-alive
Upgrade-Insecure-Requests: 1
DNT: 1
Sec-GPC: 1\r\n\r\n
hello=2&yello=a""")
    print(request.toString())
    request.setParams(dello=4)
    print(request.parameters)
