from net.WifiConfig import WifiConfig

def print_log(class_object, line, prefix = None):
    print("[{CLASSNAME}]{PREFIX}: {LINE}".format(CLASSNAME=class_object.__class__.__name__, LINE=line, PREFIX="" if prefix is None else "["+prefix+"]"))
   
def print_error(class_object, line):
    print_log(class_object, line, "ERROR")
    
def print_warning(class_object, line):
    print_log(class_object, line, "WARNING")
