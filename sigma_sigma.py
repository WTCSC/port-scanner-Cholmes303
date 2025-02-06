# Used to recognize IP addresses and CIDR notation.
import ipaddress
# Used to run system commands.
import subprocess
# Used to determine the OS.
import platform
# Used to search for patterns in strings.
import re
# Used for time the program takes to run.
import time

def ping_host(ip):
    """Pings a host and returns the status and response time."""
    try:
        # Determine OS-specific ping command.
        if platform.system().lower() == "windows":
            # Commands for Windows.
            cmd = ["ping", "-n", "1", "-w", "1000", ip]  
        else:
            # Commands for macOS and Linux.
            cmd = ["ping", "-c", "1", "-W", "1", ip]  

        # Run the ping command and capture the output.
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Check if the command was successful.
        if result.returncode != 0:
            # Capture error messages.
            return "ERROR", result.stderr.strip()  

        # Search for the response time in the output.
        match = re.search(r"time[=<]([\d.]+) ?ms", result.stdout)
        
        # If the response time is found, return it.
        if match:
            response_time = match.group(1) + "ms"
            return "UP", response_time
        # If no response time is found, return "No response".
        else:
            return "DOWN", "No response"

    except Exception as e:
        return "ERROR", str(e)

def get_active_hosts(cidr):
    """Scans the given network and reports host status."""
    try:
        # Allows for any IPv4 input with CIDR (strict=False).
        network = ipaddress.IPv4Network(cidr, strict=False)
        print(f"\nScanning network {cidr}...\n")

        results = []

        # Sets the count of each occurrence. 
        up_count = down_count = error_count = 0
        # Start timer uses Epoch time. 
        start_time = time.time()

        # Iterate over all valid hosts.
        for ip in network.hosts():
            # Ping the host and get the status and message.
            status, message = ping_host(str(ip))

            # Print the IP address, status, and message.
            print(f"{ip} - {status.ljust(6)} ({message})")

            # Count occurrences of UP, DOWN, or ERROR.
            if status == "UP":
                up_count += 1
            elif status == "DOWN":
                down_count += 1
            else:
                error_count += 1

            # Adds IP address that was found.
            # IP's status (UP, DOWN, or ERROR).
            # Message (response time in milliseconds, no response, or network not reachable).
            results.append((ip, status, message))

            
        # Print summary of IP networks from CIDR.
        print(f"\nScan complete. Found {up_count} active hosts, {down_count} down, {error_count} errors.")

        # Prints how long it takes for the program to run. 
        print(f"time: {time.time() - start_time}")
    # Checks for valid IPv4 CIDR notation (e.g. 192.168.1.0/24).
    except ValueError as e:
        print(f"Invalid CIDR notation: {e}")

# If the script is run directly, prompt the user for input.
if __name__ == "__main__":
    cidr_input = input("Enter CIDR notation (e.g., 192.168.1.0/24): ")
    get_active_hosts(cidr_input)
