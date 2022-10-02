from asyncore import read
from os import listdir

from net.www.Webserver import Webserver


if __name__ == "__main__":
    Webserver().start()