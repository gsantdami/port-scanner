import socket 
import sys
import time
import threading
import argparse
import queue


from utils.colors import Colors
from utils.art import art
from helpers.read_data import read_csv
from helpers.get_timeout import get_timeout
    
    
def argument_parser():
    parser = argparse.ArgumentParser(
        description=f'{Colors.RED} Fast port scanner. {Colors.RESET}'
    )
    parser.add_argument('-t', '--target', dest='host', required=True, help='Target IP or domain.')
    parser.add_argument('-o', '--output', dest='output', default=None, help='File to save open ports. (default: none)')
    parser.add_argument('--timeout', dest='timeout', default=None, help='Timeout in ms per port. (default: auto via ping)')
    parser.add_argument('--threads', dest='threads', default=30, help='Number of worker threads. (default: 30)')
    parser.add_argument('-n', dest='numberPorts', required=True, help='Number of ports to be scanned')
    
    return parser.parse_args()
    
    
class PortScanner():
    def __init__(self, host, output, timeout_ms, numberPorts, num_threads):
        self.host = host
        self.output = output
        self.timeout_ms = float(timeout_ms)
        self.numberPorts = int(numberPorts)
        self.num_threads = int(num_threads)
        
        port_list = read_csv(self.numberPorts)
        
        self.port_queue: queue.Queue[int] = queue.Queue()
        for p in port_list:
            self.port_queue.put(p)
            
        self.result_lock = threading.Lock()
        self.file_lock = threading.Lock()
        
        self.open_ports = []
        self.error:str | None = None
        
        self.stop_event = threading.Event()
        
        
    def run(self):
        threads = [
            threading.Thread(target=self._worker, daemon=True)
            for i in range(self.num_threads)
        ]
        
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
            
        if(self.error):
            print(self.error)
            sys.exit(1)
            
        return sorted(self.open_ports)
        
        
    def _worker(self):
        while not self.stop_event.is_set():
            try:
                port = self.port_queue.get_nowait()
            except queue.Empty:
                break
            self._probe(port)
            
            
    def _probe(self, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout_ms/1000)
                status = sock.connect_ex((self.host, port))
            
            if status == 0:
                self._save_port(port)
            
        except KeyboardInterrupt:
            self.stop_event.set()
            print(f'\n{Colors.RED}[!]  Operation canceled by the user.{Colors.RESET}')
            sys.exit(0)
            
        except socket.gaierror:
            self.stop_event.set()
            with self.result_lock:
                self.error = f'{Colors.RED}[!] Please verify the domain - getaddrinfo failed.{Colors.RESET}'
        except OSError:
            pass
    
    
    def _save_port(self, port):
        print(f'{Colors.BOLD}{Colors.GREEN}[+]    {Colors.RESET}{Colors.YELLOW}{port:<5} -> Open')
        
        with self.result_lock:
            self.open_ports.append(port)
            
            if self.output:
                with self.file_lock:
                    with open(self.output, 'a') as fh:
                        fh.write(f'{port}\n')
                    


def main():
    start = time.time()
    args = argument_parser()
    
    print(art)
    
    print(f'\n {Colors.PURPLE} PINGING ON DOMAIN... {Colors.RESET}')
    timeout_ms = float(args.timeout) if args.timeout else get_timeout(args.host)
    
    print(f'[{Colors.BLUE} DOMAIN{Colors.RESET} ]: [{Colors.PURPLE}{args.host}{Colors.RESET}]')
    print(f'[{Colors.BLUE} TIMEOUT{Colors.RESET} ]: [{Colors.PURPLE}{args.timeout}{Colors.RESET}]')
    print(f'[{Colors.BLUE} THREADS{Colors.RESET} ]: [{Colors.PURPLE}{args.threads}{Colors.RESET}]')
    print(f'\n {Colors.PURPLE}================== {Colors.RESET}{Colors.BOLD}{Colors.PURPLE}RESULTS =================={Colors.RESET}')
    
    scanner = PortScanner(
        host=args.host,
        timeout_ms=timeout_ms,
        num_threads=args.threads,
        output=args.output,
        numberPorts=args.numberPorts
    )
    open_ports = scanner.run()
    
    elapsed = time.time() - start
    port_count = args.numberPorts
    
    print(f'\n{Colors.BOLD}{Colors.GREEN}[#]{Colors.RESET}{Colors.PURPLE} {len(open_ports)} Open ports')
    print(f'{Colors.BOLD}{Colors.GREEN}[i]{Colors.RESET}{Colors.PURPLE}{port_count} Scanned ports {Colors.RESET}')
    if args.output: 
        print(f'{Colors.BOLD}{Colors.GREEN}[!]Exported to {Colors.RESET}{Colors.PURPLE}{args.output}{Colors.RESET}')
    print(f'\n{Colors.BOLD}{Colors.GREEN}Execution time: {Colors.RESET}{Colors.PURPLE}{elapsed:,.3f}{Colors.RESET}')
    
if __name__ == "__main__":
    main()