from net.WifiConfig import WifiConfig

def print_log(class_object, line, prefix = None):
    print("[{CLASSNAME}]{PREFIX}: {LINE}".format(CLASSNAME=class_object.__class__.__name__, LINE=line, PREFIX="" if prefix is None else "["+prefix+"]"))
   
def print_error(class_object, line):
    print_log(class_object, line, "ERROR")
    
def print_warning(class_object, line):
    print_log(class_object, line, "WARNING")

class __Logger:
    def log(self, class_object_or_str, line, prefix = None):
        class_name = class_object_or_str.__class__.__name__ if not isinstance(class_object_or_str, str) else class_object_or_str
        
        print("[{CLASSNAME}]{PREFIX}: {LINE}".format(CLASSNAME=class_name, LINE=line, PREFIX="" if prefix is None else "["+prefix+"]"))
   
    def error(self, class_object_or_str, line):
        self.log(class_object_or_str, line, "ERROR")
        
    def warning(self, class_object_or_str, line):
        self.log(class_object_or_str, line, "WARNING")

Logger = __Logger()