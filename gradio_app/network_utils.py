import socket
import platform
import subprocess
import re

def get_local_ip():
    """Get the local IP address of the machine on the network"""
    system = platform.system().lower()
    
    # Windows method
    if system == 'windows':
        try:
            # Run ipconfig and capture output
            output = subprocess.check_output("ipconfig", universal_newlines=True)
            
            # First look for wireless connections
            # IPv4 pattern with surrounding context
            wireless_matches = re.findall(r"Wireless LAN adapter.*?IPv4 Address.*?: (192\.168\.\d+\.\d+|10\.\d+\.\d+\.\d+)", 
                                        output, re.DOTALL)
            
            if wireless_matches:
                return wireless_matches[0]
                
            # Then look for ethernet connections
            ethernet_matches = re.findall(r"Ethernet adapter.*?IPv4 Address.*?: (192\.168\.\d+\.\d+|10\.\d+\.\d+\.\d+)", 
                                        output, re.DOTALL)
            
            if ethernet_matches:
                return ethernet_matches[0]
                
            # Fall back to any IPv4 address with preferred prefixes
            ip_matches = re.findall(r"IPv4 Address.*?: (192\.168\.\d+\.\d+|10\.\d+\.\d+\.\d+)", output)
            
            if ip_matches:
                return ip_matches[0]
        except Exception as e:
            print(f"Error getting IP with ipconfig: {e}")
            
    # Linux/Mac method
    else:
        try:
            # Try ifconfig first (older Linux/Mac systems)
            try:
                output = subprocess.check_output(["ifconfig"], universal_newlines=True)
            except:
                # If ifconfig fails, try ip addr (newer Linux systems)
                output = subprocess.check_output(["ip", "addr"], universal_newlines=True)
            
            # Look for preferred IP patterns
            ip_matches = re.findall(r"inet (192\.168\.\d+\.\d+|10\.\d+\.\d+\.\d+|172\.(1[6-9]|2[0-9]|3[0-1])\.\d+\.\d+)", 
                                 output)
            
            if ip_matches:
                # Filter out 127.0.0.1
                for ip in ip_matches:
                    if not ip.startswith("127."):
                        return ip
        except Exception as e:
            print(f"Error getting IP with ifconfig/ip addr: {e}")
    
    # If all else fails, fall back to the socket method
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        pass
            
    # Last resort fallback to loopback
    return "127.0.0.1"

def get_server_url(port):
    """Get the server URL with local IP"""
    local_ip = get_local_ip()
    return f"http://{local_ip}:{port}/" 