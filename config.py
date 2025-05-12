import socket
import nmap
import netifaces

def get_local_ip(interface):
    try:
        local_ip = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
    except (KeyError, IndexError):
        local_ip = '127.0.0.1'
    return local_ip

def get_interfaces():
    interfaces = netifaces.interfaces()
    interface_info = {}
    for iface in interfaces:
        try:
            addr = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']
            interface_info[iface] = addr
        except (KeyError, IndexError):
            continue
    return interface_info

def scan_network(network_range):
    nm = nmap.PortScanner()
    nm.scan(network_range, arguments='-p 80,443,3306,22,21,139,445')
    devices = {}

    for host in nm.all_hosts():
        open_ports = [port for port in nm[host].all_tcp() if nm[host]['tcp'][port]['state'] == 'open']
        devices[host] = open_ports

    return devices

def get_username_list():
    with open('./src/usernames.txt', 'r') as file:
        usernames = [line.strip() for line in file]
    return usernames

def get_password_list():
    with open('./src/passwords.txt', 'r') as file:
        passwords = [line.strip() for line in file]
    return passwords

def select_interface():
    interfaces = netifaces.interfaces()
    print("Available network interfaces:")
    for i, iface in enumerate(interfaces):
        print(f"{i}: {iface}")
    
    choice = int(input("Select the interface number to scan: "))
    return interfaces[choice]
