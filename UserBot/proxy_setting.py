import winreg

def get_proxy_settings() -> dict | None:
    """
    get proxy setting from windows
    :return: {'scheme': str, 'hostname': str, 'port': int} | None if exception raised
    """
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Software\Microsoft\Windows\CurrentVersion\Internet Settings")
        proxy_server = winreg.QueryValueEx(reg_key, "ProxyServer")[0]
        proxy_enable = winreg.QueryValueEx(reg_key, "ProxyEnable")[0]
        if proxy_enable == 1:
            scheme = 'http'
            if proxy_server.startswith('socks5'):
                scheme = 'socks5'
            host_name, port = proxy_server.split(':')
            proxy_settings = {'scheme': scheme, 'hostname': host_name, 'port': int(port)}
            return proxy_settings
        else:
            return None
    except Exception as e:
        print('error on getting proxy')
        return None