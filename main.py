import socket 
import time
import threading
import argparse
import queue


from helpers.read_data import read_csv

from pythonping import ping

class Colors:
    """ ANSI color codes """
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    BOLD = "\033[1m"
    ITALIC = "\033[3m"
    RESET = "\033[0;0;0m"
    
def argument_parser():
    parser = argparse.ArgumentParser(
        description=f'{Colors.RED} Fast port scanner. {Colors.RESET}'
    )
    parser.add_argument('-t', '--target', dest='host', required=True, help='Target IP or domain.')
    

ports = read_csv("data/top10k.csv")
print(ports)