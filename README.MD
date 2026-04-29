# Port Scanner

Fast mulithreaded port scanner written in python.

A lightweight tool designed for speed and simplicity, capable of scanning thousands of ports quickly using concurrent threads.

## Installation

🔹 Recommended (global installation with pipx)
### Install pipx (if not installed)
```bash
sudo apt install pipx
pipx ensurepath
```

### Install the tool
```bash 
pipx install git+https://github.com/SEU_USUARIO/portscanner.git
```

## Development install

```bash
git clone https://github.com/gsantd/portscanner.git
cd port-scanner
python -m venv .venv 
source .venv/bin/activate 
pip install -e .
```

## Usage

```bash
portscan -t <target> -n <number_of_ports> [options]
```

Example: 
```bash
portscan -t nmap.scanme.org -n 1000 -o output.txt
```

If you want to use sudo for auto via ping, use:
```bash 
sudo env "PATH=$PATH" portscan -t <target> -n <number_of_ports> [options]
```



## Options

| Argument | Description | Required | Default |
|----------|-------------|----------|-------------|
| `-t`, `--target` | Target IP or domain | True | - |
| `-n` | Number of ports to scan (max: 10000) | True | - |
| `--threads` | Number of threads | False | 30 |
| `--timeout` | Timeout per port in ms | False | auto: via ping or 1000ms |
| `-o`, `--output` | Save open ports to file | False | None |

## Notes 

This scanner prioritizes speed, which may lead to missed ports under certain network conditions.
For highly accurate results, consider using tools like Nmap.