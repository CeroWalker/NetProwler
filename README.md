# NetProwler

Kapadokya Üniversitesi Bilişim Güvenliği Teknolojisi Bitirme Projesi  
Geliştiriciler: [CeroWalker](https://github.com/CeroWalker), [Kalyke1](https://github.com/Kalyke1)

## Proje Hakkında

**NetProwler**, ağ üzerindeki cihazları ve servisleri keşfetmek, zafiyet taraması yapmak ve brute-force saldırılarını denemek için geliştirilen modern bir ağ güvenliği aracıdır. Kullanıcı dostu bir arayüz ile Python ve HTML teknolojileri kullanılarak tasarlanmıştır.

## Temel Özellikler

- **Ağ Taraması:** Belirlenen arayüz üzerinden yerel ağı tarar, aktif cihazları ve açık portları bulur.
- **Servis Tespiti ve Zafiyet Analizi:** FTP, SSH, HTTP ve SMB servislerini algılar ve servis bazlı zafiyet kontrolleri yapar.
- **Brute-force Saldırıları:** Otomatik olarak FTP, SSH, HTTP login ve SMB servislerine brute-force saldırılarını deneyebilir.
- **Kolay Kullanım:** Web tabanlı kullanıcı arayüzü sayesinde ağ taraması başlatmak ve sonuçları takip etmek çok kolaydır.
- **Sonuçların Dışa Aktarılması:** Tarama sonuçlarını JSON veya DOCX olarak dışa aktarabilirsiniz.

## Kurulum

1. **Gereksinimler:**
   - Python 3.8+
   - Flask
   - netifaces
   - Diğer bağımlılıklar için:  
     ```bash
     pip install -r requirements.txt
     ```

2. **Projeyi Klonlayın:**
   ```bash
   git clone https://github.com/CeroWalker/NetProwler.git
   cd NetProwler
   ```

3. **Web Sunucusunu Başlatın:**
   ```bash
   python web_server.py
   ```
   Varsayılan olarak `http://localhost:5000` adresinden arayüze erişebilirsiniz.

## Kullanım

1. Tarayıcıdan web arayüzünü açın.
2. Ağ arayüzünü seçin ve "Taramayı Başlat" butonuna tıklayın.
3. Tarama tamamlandığında sonuçları ekranda görüntüleyebilir, isterseniz JSON veya DOCX olarak indirebilirsiniz.

## Dizin Yapısı

- `index.py` : Komut satırından çalışan ana tarama betiği.
- `web_server.py` : Flask tabanlı web sunucusu ve API.
- `templates/index.html` : Web arayüzü.
- `tools/` : Servis ve brute-force işlemleri için yardımcı modüller.

## Katkı

Katkıda bulunmak için lütfen bir issue açın veya pull request göndermekten çekinmeyin.

## Lisans

Bu proje sadece eğitim amaçlıdır. Ticari kullanım veya yetkisiz ağlarda kullanımı sorumluluk doğurabilir.

## Etik ve Yasal Uyarı

> **Uyarı:** NetProwler, yalnızca eğitim, araştırma ve yasal izin alınmış test ortamlarında kullanılmak üzere geliştirilmiştir. Gerçek ağlarda veya izinsiz sistemlerde kullanımı yasa dışı olabilir ve etik değildir.  
> 
> Bu aracı kullanmadan önce mutlaka sistem sahibi veya yöneticisinden izin alınız. Yasal olmayan kullanımlardan doğabilecek tüm sorumluluk kullanıcıya aittir. Geliştiriciler hiçbir şekilde kötüye kullanımdan sorumlu tutulamaz.

---

Herhangi bir öneri veya hata bildirimi için [GitHub Issues](https://github.com/CeroWalker/NetProwler/issues) üzerinden iletişime geçebilirsiniz.

## Kaynakça ve Kullanılan Teknolojiler

- **Python**  
  [https://www.python.org/](https://www.python.org/)
- **Flask** (web framework)  
  [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
- **netifaces** (ağ arayüzü yönetimi için)  
  [https://pypi.org/project/netifaces/](https://pypi.org/project/netifaces/)
- **Nmap** (ağ taraması için)  
  [https://nmap.org/](https://nmap.org/)
  [https://pypi.org/project/python-nmap/](https://pypi.org/project/python-nmap/)
- **ftplib** (Python standart kütüphanesinde FTP işlemleri için)  
  [https://docs.python.org/3/library/ftplib.html](https://docs.python.org/3/library/ftplib.html)
- **paramiko** (SSH işlemleri için)  
  [https://www.paramiko.org/](https://www.paramiko.org/)
  [https://pypi.org/project/paramiko/](https://pypi.org/project/paramiko/)
- **SMBConnection** (SMB için)  
  [https://pysmb.readthedocs.io/en/latest/api/smb_SMBConnection.html](https://pysmb.readthedocs.io/en/latest/api/smb_SMBConnection.html)
- **requests** (HTTP istekleri için)  
  [https://docs.python-requests.org/en/latest/](https://docs.python-requests.org/en/latest/)

Ek olarak, projenin geliştirilmesinde çeşitli açık kaynak kütüphaneler ve resmi dokümantasyonlardan yararlanılmıştır.
