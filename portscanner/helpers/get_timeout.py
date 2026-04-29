import sys
from portscanner.utils.colors import Colors
from pythonping import ping

def get_timeout(host):
    try:
        result = ping(target=host, count=1, timeout=5)
        return float(result.rtt_avg_ms) + 200
    except KeyboardInterrupt:
        print(f'\n{Colors.RED}[!]  Operation canceled by the user.{Colors.RESET}')
        sys.exit(0)
    except PermissionError:
        print(f'{Colors.YELLOW}[!] Ping requires sudo. Using default timeout (1000ms).{Colors.RESET}')
        return 1000
    except Exception as e:
        print(f'{Colors.YELLOW}[!] Could not ping host. Using default timeout (1000ms).{Colors.RESET}')
        return 1000