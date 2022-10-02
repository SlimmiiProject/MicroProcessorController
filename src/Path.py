from os import listdir
from re import search


def dirname(path):
    return search(r"(.*?)(\/|\\)(?=(.*?)$)", path).group()
    
def filename(path):
    return search(r"(?<=(\\|\/))(.*?)$", path).group()

def readFileLine(path):
    file, output = None
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
    file, output = None
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
    file, output = None
    try:
        file = open(path, "r")
        output = file.read()
    except OSError as e:
        print(e)
    finally:
        if file is not None:
            file.close()
        return output
    
def writeFile(path, data):
    root = dirname(path)
    name = filename(path)
    
    file = None
    try:
        file = open(path, "w" if name in listdir(root) else "x")
        file.write(data)
    except OSError as e:
        print(e)
    finally:
        if file is not None:
            file.close()
    