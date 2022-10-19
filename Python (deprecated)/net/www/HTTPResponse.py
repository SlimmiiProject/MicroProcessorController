from re import search

from components.layout.Footer import Footer
from components.layout.Header import Header
from components.layout.Navbar import Navbar

from net.www.mime.MimeBaseTypes import MimeBaseTypes
from net.www.mime.MimeTypes import MimeTypes

from utils.Path import readFileLines, readFileBytes
from net.www.HTTPHeader import HTTPHeader




class HTTPResponse(HTTPHeader):
    exit_callback = None
    
    def __init__(self, request):
        super().__init__(request.toString(0))
        self.setParams(**request.parameters)
        self.setParams(**{
            "HEADER": Header(),
            "NAVBAR": Navbar(),
            "FOOTER": Footer(),
        })
        

    def __parsePageParameters(self, page, **kwargs):
        assert isinstance(page, str)
        
        html = page
        while html is not None: 
            # Zoek {KEY_NAAM} in de pagina broncode. 
            match =  search(r"\{%(.*?)%\}", html)
            if match is None:
                break

            # Parse match en key voor parameter hashmap.
            match = match.group(0)
            key = str(match)[2:-2]
            
            html = html.replace(match, kwargs[key] if key in kwargs.keys() else f"PARAMETER_{key}_UNDEFINED")
        
        return html
            
    def getPublicFile(self):
        file_path = "{ROOT}{NAME}".format(ROOT="/public", NAME=self.absolute_path)
        file_ext = None
        if self.file_extension is None:
            if len(self.absolute_path) == 1:
                file_path += "index"
                
            file_path += ".html"
            self.content_type = "text/html"
        
        file_ext = f".{file_path.split(".")[-1]}"
            
        content = None
        if file_ext in MimeBaseTypes[str]:
            content = "".join(readFileLines(file_path))
            content = self.__parsePageParameters(content, **self.parameters)
        elif file_ext in MimeBaseTypes[bytes]:
            content = readFileBytes(file_path)
        else:
            print(f"Failed to fetch data\Path: {file_path}")
            
        return content
    
        
    def getFile(self, endpoint, **kwargs):
        return self.getPublicFile()
    
 
    def send(self, client):
        data = bytes(self.data, "utf-8") if isinstance(self.data, str) else self.data
        client.send(bytes(self.toString(1), "utf-8"))
        
        if data is not None:
            client.send(data)
    

    
