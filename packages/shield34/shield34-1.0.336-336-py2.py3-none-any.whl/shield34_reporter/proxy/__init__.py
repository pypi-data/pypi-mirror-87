import json
import os
import platform
import socket
import tempfile
import time

from shield34_reporter.consts.shield34_properties import Shield34Properties
from shield34_reporter.container.run_report_container import RunReportContainer
from shield34_reporter.proxy.browsermobproxy import Server
from shield34_reporter.utils.logger import Shield34Logger
from shield34_reporter.utils.network_utils import NetworkUtils


def get_browsermob_proxy_server():
    browser_mob_server = get_existing_browsermob()
    if browser_mob_server is None or not browser_mob_proxy_is_listening(browser_mob_server, retry_count=5):
        Shield34Logger.logger.console("Created Shield34 proxy server")
        wait_for_lock_create_proxy_to_be_released(timeout=10)
        lock_create_proxy()
        browser_mob_server = start_new_browsermob()
        release_lock_create_proxy()
    return browser_mob_server


def get_existing_browsermob():
    try:
        proxy_data_filepath = get_shield34_proxy_data_filename()
        proxy_exec_path = add_browsermob_to_path()
        if os.path.exists(proxy_data_filepath):
            browser_mob_server_config = read_json_from_file(proxy_data_filepath)
            if browser_mob_server_config.get('port', None) is not None and browser_mob_server_config.get('pid',None) is not None:
                browser_mob_server = Server(proxy_exec_path, options={'port': browser_mob_server_config['port']})
                browser_mob_server.host = get_local_ip()
                browser_mob_server.command += ['--address=' + get_local_ip(), "--ttl=3600"]
                browser_mob_server.pid = browser_mob_server_config['pid']
                return browser_mob_server
    except Exception:
        pass
    return None


def start_new_browsermob():
    browser_mob_server_config = {}
    proxy_data_filepath = get_shield34_proxy_data_filename()
    proxy_exec_path = add_browsermob_to_path()
    proxy_server_port = NetworkUtils.get_random_port(get_local_ip())
    browser_mob_server = Server(proxy_exec_path, options={'port': proxy_server_port})
    browser_mob_server.host = get_local_ip()
    browser_mob_server.command += ['--address=' + get_local_ip(), "--ttl=3600"]
    browser_mob_server.start()
    browser_mob_server_config['port'] = proxy_server_port
    browser_mob_server_config['pid'] = browser_mob_server.process.pid
    browser_mob_server.pid = browser_mob_server.process.pid
    try:
        write_json_to_file(proxy_data_filepath, browser_mob_server_config)
    except Exception as e:
        pass
    return browser_mob_server


def get_local_ip():
    try:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except Exception :
        return "127.0.0.1"


def write_json_to_file(file_path, dictjson):
    with open(file_path, 'w') as file:
        file.write(json.dumps(dictjson))
    file.close()


def browser_mob_proxy_is_listening(browser_mob_server, retry_count=60):
    count = 0
    while not browser_mob_server._is_listening():
        time.sleep(0.5)
        count += 1
        if count == retry_count:
            return False
    return True


def add_browsermob_to_path():
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(ROOT_DIR, 'proxy', 'browsermob-proxy-2.1.4', 'bin')
    os.environ["PATH"] += os.pathsep + path
    try:
        if platform.system() != 'Windows':
            file = os.path.join(path, "browsermob-proxy")
            st = os.stat(file)
            os.chmod(file, st.st_mode | os.stat.S_IEXEC)
    except Exception as e:
        pass
    return os.path.join(path,'browsermob-proxy')


def read_json_from_file(file_path):
    with open(file_path, 'r') as file:
        dictjsonstr = file.read()
    file.close()
    return json.loads(dictjsonstr)


def get_shield34_proxy_data_filename():
    temp_dir = tempfile.gettempdir()
    filepath = os.path.join(temp_dir, 'shield34_proxy.dat')
    return filepath


def lock_create_proxy():
    write_lock_file(get_shield34_proxy_lock_filename())


def release_lock_create_proxy():
    file =get_shield34_proxy_lock_filename()
    if os.path.exists(file):
        os.remove(file)


def wait_for_lock_create_proxy_to_be_released(timeout=10):
    counter = 0
    while os.path.exists(get_shield34_proxy_lock_filename()):
        time.sleep(1)
        counter = counter + 1
        if counter > timeout:
            release_lock_create_proxy()
            break


def get_shield34_proxy_lock_filename():
    temp_dir = tempfile.gettempdir()
    filepath = os.path.join(temp_dir, 'shield34_proxy.lck')
    return filepath


def write_lock_file(file_path):
    with open(file_path, 'w') as file:
        file.write("")
    file.close()


def get_shield34_proxy(upsream_chained_proxy=None):
    from shield34_reporter.utils.reporter_proxy import ProxyServerNotInitializedException, \
        create_new_proxy_instance
    proxies_count = len(RunReportContainer.get_current_block_run_holder().proxyServers)
    proxy_server = None
    if proxies_count > 0:
        proxy_server = RunReportContainer.get_current_block_run_holder().proxyServers[proxies_count-1]

    if upsream_chained_proxy is not None:
        proxy_server = create_new_proxy_instance(upsream_chained_proxy)
        RunReportContainer.get_current_block_run_holder().proxyServers.append(proxy_server)


    if proxy_server is None:
        raise ProxyServerNotInitializedException()

    default_proxy = proxy_server.proxy
    http_proxy = "http://{}".format(default_proxy)
    https_proxy = "http://{}".format(default_proxy)
    ftp_proxy = "http://{}".format(default_proxy)
    proxyDict = {
        "http": http_proxy,
        "https": https_proxy,
        "ftp": ftp_proxy
    }
    return proxyDict

