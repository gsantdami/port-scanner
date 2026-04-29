import sys
from utils.colors import Colors
from pythonping import ping

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