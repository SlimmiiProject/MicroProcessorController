from asyncore import read
from os import listdir

from torch import randint
from net.www.Webserver import Webserver

import random
import sys

#import machine

class __Device: 
    __SERIAL_LENGTH = 64

    @property
    def serial_no(self):
        if "serial" not in listdir("./"):
            writer = open("serial", "x")
            writer.write("".join([str(random.randint(0, 9)) if i % 2 == 0 else chr(random.randint(64, 64+26)) for i in range(self.__SERIAL_LENGTH)]))
            writer.close()

        reader = open("serial", "r")
        output = reader.readline()
        reader.close()

        assert len(output) == self.__SERIAL_LENGTH
        return output

    def soft_reset(self):
        sys.exit()

    def hard_reset(self):
        pass
        #machine.reset()


if __name__ == "__main__":
    print(__Device().serial_no)
    Webserver().start()