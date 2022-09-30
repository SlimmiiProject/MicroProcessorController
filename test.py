from asyncore import read
from os import listdir
import json

# Fetch wifi config of creer indien nodig, gebruik XOR flip op karakters zodat data niet ruw wordt neergeschreven.
conInfo = """{"ssid":"", "password":""}"""
if not "wifi.bin" in listdir("./"):
    writer = open("./wifi.bin", "x")
    writer.write("".join([chr(ord(i)^129) for i in conInfo]))
    writer.close()

reader = open("./wifi.bin", "r")
print(json.loads("".join([chr(ord(i)^129) for i in reader.readline()]))["ssid"])
reader.close()