import ipaddress
import subprocess
import platform
import re
import time
import socket
import argparse

def ping_host(ip):
    """Pings a host and returns the status and response time."""
    try:
        if platform.system().lower() == "windows":
            cmd = ["ping", "-n", "1", "-w", "1000", ip]  
        else:
            cmd = ["ping", "-c", "1", "-W", "1", ip]  
        
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=2)
        
        if result.returncode != 0:
            return "DOWN", "No response"
        
        match = re.search(r"time[=<]([\d.]+) ?ms", result.stdout)
        if match:
            response_time = match.group(1) + "ms"
            return "UP", response_time
        else:
            return "DOWN", "No response"
    except subprocess.TimeoutExpired:
        return "ERROR", "Ping timeout"
    except Exception as e:
        return "ERROR", str(e)

def scan_ports(ip, ports=[22, 80, 443]):
    """Scans specified ports on a given IP and returns open ports."""
    open_ports = []
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            if s.connect_ex((ip, port)) == 0:
                open_ports.append(port)
    return open_ports

def get_active_hosts(cidr, scan_ports_flag=False):
    """Scans the network and reports active hosts."""
    try:
        network = ipaddress.IPv4Network(cidr, strict=False)
        print(f"\nScanning network {cidr}...\n")
        results = []
        up_count = down_count = error_count = 0
        start_time = time.time()

        for ip in network.hosts():
            status, message = ping_host(str(ip))
            if status == "UP":
                up_count += 1
                print(f"{ip} - {status} ({message})", end="")
                if scan_ports_flag:
                    open_ports = scan_ports(str(ip))
                    if open_ports:
                        print(f" - Open ports: {', '.join(map(str, open_ports))}")
                    else:
                        print(" - No open ports")
                else:
                    print()
            elif status == "DOWN":
                down_count += 1
            else:
                error_count += 1
            results.append((ip, status, message))
        
        print(f"\nScan complete. Found {up_count} active hosts, {down_count} down, {error_count} errors.")
        print(f"Time elapsed: {time.time() - start_time:.2f} seconds")
    except ValueError as e:
        print(f"Invalid CIDR notation: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Network Scanner with Optional Port Scanning")
    parser.add_argument("cidr", help="CIDR notation (e.g., 192.168.1.0/24)")
    parser.add_argument("-p", action="store_true", help="Scan open ports on active hosts")
    args = parser.parse_args()
    get_active_hosts(args.cidr, args.p)
