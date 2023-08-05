import uuid
import socket


def get_mac_address():
    node = uuid.getnode()
    mac = uuid.UUID(int=node).hex[-12:]
    return mac


def get_host_name():
    return socket.gethostname()


def get_host_ip():
    """通过 UDP 获取本机 IP，目前见过最优雅的方法"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def get_ip_address(request):
    ip_address = request.headers.get('x-forwarded-for')
    if not ip_address or ip_address == 'unknown':
        ip_address = request.headers.get('Proxy-Client-IP')
    if not ip_address or ip_address == 'unknown':
        ip_address = request.headers.get('WL-Proxy-Client-IP')
    if not ip_address or ip_address == 'unknown':
        ip_address = request.remote
        if ip_address == '127.0.0.1':
            ip_address = get_host_ip()
    if not ip_address and len(ip_address) > 15:
        ip_address = ip_address.split(',')[0]
    return ip_address
