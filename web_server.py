from flask import Flask, render_template, request, jsonify
from tools.web import find_login_page, web_brute_force
from tools.ftp import check_anonymous_access, ftp_brute_force
from tools.ssh import ssh_brute_force
from tools.smb import check_smb_ports, enum_smb_shares, smb_brute_force, check_smb_version
from config import get_username_list, get_password_list, select_interface, get_local_ip, scan_network
import netifaces
import threading
import queue

app = Flask(__name__)
scan_results = queue.Queue()
current_status = "Hazır"

def scanner_thread(interface):
    global current_status
    results = {}
    
    try:
        local_ip = get_local_ip(interface)
        results['local_ip'] = local_ip
        current_status = f"IP adresi alındı: {local_ip}"

        network_range = local_ip.rsplit('.', 1)[0] + ".0/24"
        results['network_range'] = network_range
        current_status = f"Ağ taraması başlatıldı: {network_range}"

        devices = scan_network(network_range)
        results['devices'] = {}

        for ip, ports in devices.items():
            device_info = {
                'ports': ports,
                'services': [],
                'brute_results': []  # Yeni eklenen alan
            }

            if 21 in ports:
                current_status = f"FTP taraması: {ip}"
                anon_access = check_anonymous_access(ip)
                device_info['services'].append({
                    'service': 'FTP',
                    'anonymous_access': anon_access
                })
                
                # FTP Brute Force
                username_list = get_username_list()
                password_list = get_password_list()
                current_status = f"FTP brute force deneniyor: {ip}"
                ftp_results = ftp_brute_force(ip, username_list, password_list)
                if ftp_results:
                    device_info['brute_results'].append({
                        'service': 'FTP',
                        'credentials': ftp_results
                    })

            if 22 in ports:
                current_status = f"SSH taraması: {ip}"
                device_info['services'].append({
                    'service': 'SSH'
                })
                
                # SSH Brute Force
                username_list = get_username_list()
                password_list = get_password_list()
                current_status = f"SSH brute force deneniyor: {ip}"
                ssh_results = ssh_brute_force(ip, username_list, password_list)
                if ssh_results:
                    device_info['brute_results'].append({
                        'service': 'SSH',
                        'credentials': ssh_results
                    })

            if 80 in ports:
                current_status = f"HTTP taraması: {ip}"
                login_url = find_login_page(ip)
                if login_url:
                    device_info['services'].append({
                        'service': 'HTTP',
                        'login_url': login_url
                    })
                    username_list = get_username_list()
                    password_list = get_password_list()
                    current_status = f"Web brute force deneniyor: {ip}"
                    web_results = web_brute_force(login_url, username_list, password_list)
                    if web_results:
                        device_info['brute_results'].append({
                            'service': 'HTTP',
                            'credentials': web_results
                        })

            if 139 in ports or 445 in ports:
                current_status = f"SMB taraması: {ip}"
                smb_version = check_smb_version(ip)
                shares = enum_smb_shares(ip, '', '')
                device_info['services'].append({
                    'service': 'SMB',
                    'version': smb_version,
                    'shares': shares
                })
                if not shares:
                    username_list = get_username_list()
                    password_list = get_password_list()
                    current_status = f"SMB brute force deneniyor: {ip}"
                    smb_results = smb_brute_force(ip, username_list, password_list)
                    if smb_results:
                        device_info['brute_results'].append({
                            'service': 'SMB',
                            'credentials': smb_results
                        })

            results['devices'][ip] = device_info

        current_status = "Tarama tamamlandı"
        scan_results.put(results)
    except Exception as e:
        current_status = f"Hata: {str(e)}"
        scan_results.put({'error': str(e)})

@app.route('/')
def index():
    interfaces = netifaces.interfaces()
    return render_template('index.html', interfaces=interfaces)

@app.route('/start_scan', methods=['POST'])
def start_scan():
    interface = request.form.get('interface')
    if not interface:
        return jsonify({'error': 'Interface seçilmedi'}), 400

    thread = threading.Thread(target=scanner_thread, args=(interface,))
    thread.daemon = True
    thread.start()
    
    return jsonify({'status': 'Tarama başlatıldı'})

@app.route('/status')
def status():
    return jsonify({'status': current_status})

@app.route('/results')
def results():
    if not scan_results.empty():
        return jsonify(scan_results.get())
    return jsonify({'status': 'Sonuç bekleniyor'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)