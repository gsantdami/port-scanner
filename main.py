import socket 
import sys
import time
import threading
import argparse
import queue


from utils.colors import Colors
from helpers.read_data import read_csv
    
    
def argument_parser():
    parser = argparse.ArgumentParser(
        description=f'{Colors.RED} Fast port scanner. {Colors.RESET}'
    )
    parser.add_argument('-t', '--target', dest='host', required=True, help='Target IP or domain.')
    parser.add_argument('-o', '--output', dest='output', default=None, help='File to save open ports. (default: none)')
    parser.add_argument('--timeout', dest='timeout', default=None, help='Timeout in ms per port. (default: auto via ping)')
    parser.add_argument('--threads', dest='threads', default=30, help='Number of worker threads. (default: 30)')
    parser.add_argument('-n', dest='numberPorts', default=0, help='Number of ports to eb scanned. (default: 0)')
    
    return parser.parse_args()

    
def get_timeout(host):
    try:
        result = ping(target=host, count=1, timeout=5)
        return float(result.rtt_avg_ms) + 80
    except KeyboardInterrupt:
        print(f'\n{Colors.RED}[!]  Operation canceled by the user.{Colors.RESET}')
        sys.exit(0)
    except Exception as e:
        print(f'{Colors.RED} FATAL ERROR {Colors.RESET}{e}')
        sys.exit(1)
    
    
class PortScanner():
    def __init__(self, host, output):
        self.host = host
        self.output = output
        