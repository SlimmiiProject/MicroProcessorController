from os import listdir
from re import search


def dirname(path):
    path = "/".join(path.split("/")[0:-1])
    return path if len(path) >= 1 else "/"

    
def filename(path):
    return path.split("/")[-1]

def file_exists(filepath):
    return filename(filepath) in listdir(dirname(filepath))

def readFileLine(path):
    file, output = [None, None]
    try:
        file = open(path, "r")
        output = file.readline()
    except OSError as e:
        print(e)
    finally:
        if file is not None:
            file.close()
            
        return output

def readFileLines(path):
    file, output = [None, None]
    try:
        file = open(path, "r")
        output = file.readlines()
    except OSError as e:
        print(e)
    finally:
        if file is not None:
            file.close()
        return output

def readFileBytes(path):
    file, output = [None, None]
    
    try:
        file = open(path, "rb")
        output = file.read()
    except OSError as e:
        print(e)
    finally: 
        if file is not None:
            file.close()
        return output
    
def writeFile(path, data):
    file = None
    try:
        file = open(path, "w" if file_exists(path) else "x")
        file.write(data)
    except OSError as e:
        print(e)
    finally:
        if file is not None:
            file.close()
            
            
if __name__ == "__main__":
    print(readFileBytes("/public/test.jpg"))
    