import socket
import struct
from smb.SMBConnection import SMBConnection

def check_smb_ports(ip):
    """SMB portlarının açık olup olmadığını kontrol et"""
    open_ports = []
    for port in [139, 445]:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports

def enum_smb_shares(ip, username='', password=''):
    """SMB paylaşımlarını listele"""
    try:
        # SMB bağlantısı kur
        conn = SMBConnection(username, password, 'NetProwler', 'WORKGROUP', use_ntlm_v2=True)
        if conn.connect(ip, 445):
            print(f"[ SMB ] {ip} adresine bağlantı başarılı (kullanıcı: {username or 'boş'}, şifre: {password or 'boş'})")
            
            # Paylaşımları listele
            shares = conn.listShares()
            for share in shares:
                if not share.isSpecial:
                    print(f"[ SMB ] Paylaşım bulundu: {share.name} - {share.comments}")
                    
                    # Paylaşımdaki dosyaları listeleyip görüntüleme (ek özellik)
                    try:
                        file_list = conn.listPath(share.name, '/')
                        print(f"[ SMB ] {share.name} içinde {len(file_list)} öğe bulundu")
                    except:
                        print(f"[ SMB ] {share.name} paylaşımına erişim yetkiniz yok")
            return shares
    except Exception as e:
        print(f"[ SMB ] Bağlantı hatası: {e}")
    return None

def smb_brute_force(ip, username_list, password_list):
    """SMB için brute force dene"""
    for username in username_list:
        for password in password_list:
            try:
                conn = SMBConnection(username, password, 'NetProwler', 'WORKGROUP', use_ntlm_v2=True)
                if conn.connect(ip, 445):
                    print(f"[ SMB ] Başarılı giriş: {username}:{password} -> {ip}")
                    shares = conn.listShares()
                    print(f"[ SMB ] Erişilebilir paylaşımlar: {len(shares)}")
                    conn.close()
                    return username, password
            except Exception:
                # Başarısız deneme, devam et
                continue
    print("[ SMB ] Giriş başarısız.")
    return None

def check_smb_version(ip):
    """SMB versiyonunu tespit etmeye çalış"""
    try:
        # SMB protokolü için basit bir versiyonlama kontrolü
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((ip, 445))
        
        # SMB protokol anlaşması paketi (basitleştirilmiş)
        pkt = b'\x00\x00\x00\x85\xff\x53\x4d\x42\x72\x00\x00\x00\x00\x18\x53\xc0'
        pkt += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xfe'
        pkt += b'\x00\x00\x00\x00\x00\x62\x00\x02\x50\x43\x20\x4e\x45\x54\x57\x4f'
        pkt += b'\x52\x4b\x20\x50\x52\x4f\x47\x52\x41\x4d\x20\x31\x2e\x30\x00\x02'
        pkt += b'\x4c\x41\x4e\x4d\x41\x4e\x31\x2e\x30\x00\x02\x57\x69\x6e\x64\x6f'
        pkt += b'\x77\x73\x20\x66\x6f\x72\x20\x57\x6f\x72\x6b\x67\x72\x6f\x75\x70'
        pkt += b'\x73\x20\x33\x2e\x31\x61\x00\x02\x4c\x4d\x31\x2e\x32\x58\x30\x30'
        pkt += b'\x32\x00\x02\x4c\x41\x4e\x4d\x41\x4e\x32\x2e\x31\x00\x02\x4e\x54'
        pkt += b'\x20\x4c\x4d\x20\x30\x2e\x31\x32\x00'
        
        s.send(pkt)
        resp = s.recv(1024)
        
        # SMB yanıtını analiz et
        if len(resp) > 0:
            dialect_index = struct.unpack('<H', resp[36:38])[0]
            dialects = ["PC NETWORK PROGRAM 1.0", "LANMAN1.0", "Windows for Workgroups 3.1a", 
                       "LM1.2X002", "LANMAN2.1", "NT LM 0.12"]
            
            if dialect_index < len(dialects):
                version = dialects[dialect_index]
                print(f"[ SMB ] Protokol versiyonu: {version}")
                
                # SMBv1 (CIFS) kontrolü
                if "NT LM 0.12" in version:
                    print("[ SMB ] SMBv1 (potansiyel olarak tehlikeli) kullanılıyor")
                return version
        s.close()
    except Exception as e:
        print(f"[ SMB ] Versiyon tespiti hatası: {e}")
    
    return "Bilinmiyor"
