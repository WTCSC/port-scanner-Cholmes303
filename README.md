[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=18072887)

# Network Scanner with Optional Port Scanning

## Description
This Python script scans a given network for active hosts using ICMP ping requests. Optionally, it can also scan for open ports on discovered active hosts. The script supports both Windows and Unix-based operating systems and provides detailed results on host availability and response time.

## Features
- **Ping scanning**: Detects active hosts within a given network.
- **Port scanning**: Optionally scans common ports (22, 80, 443) on active hosts.
- **Cross-platform**: Works on Windows, Linux, and macOS.
- **Customizable network range**: Accepts IPv4 addresses in CIDR notation.
- **Command-line interface**: Easy to use with simple arguments.

## Prerequisites
Ensure you have Python 3 installed on your system. This script does not require additional libraries beyond the standard Python library.

## Usage
Run the script using the following command:

```bash
python3 port_scanner.py <CIDR> [-p]
```

### Arguments:
- `<CIDR>`: The network range in CIDR notation (e.g., `192.168.1.0/24`).
- `-p`: Optional flag to enable port scanning on active hosts.

### Examples:
#### Scan a network for active hosts:
```bash
python3 port_scanner.py 192.168.1.0/24
```

#### Scan a network for active hosts and check for open ports:
```bash
python3 port_scanner.py 192.168.1.0/24 -p
```

## Output Example
```
Scanning network 192.168.1.0/24...

192.168.1.1 - UP (5ms) - Open ports: 22, 80
192.168.1.2 - UP (10ms) - No open ports

Scan complete. Found 2 active hosts, 252 down, 0 errors.
Time elapsed: 3.45 seconds
```

## How It Works
1. The script parses the provided CIDR notation to identify potential host IPs.
2. It pings each IP to check if the host is up.
3. If the `-p` flag is used, it scans ports 22 (SSH), 80 (HTTP), and 443 (HTTPS) on active hosts.
4. The results are displayed in the terminal, showing the status and response times of each host.

## Limitations
- Requires administrator/root privileges for some network configurations.
- ICMP requests might be blocked by firewalls, leading to false negatives.
- The port scanning feature only checks predefined ports; it does not perform a full port scan.

