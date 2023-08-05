import socket
import sys
import time
import urllib

from shield34_reporter import proxy
from shield34_reporter.auth.sdk_authentication import SdkAuthentication
from shield34_reporter.consts.shield34_properties import Shield34Properties
from shield34_reporter.proxy import get_local_ip
from shield34_reporter.utils.logger import Shield34Logger
from shield34_reporter.utils.network_utils import NetworkUtils


class ProxyServerNotInitializedException(Exception):
    pass


class ProxyManagementServerNotInitializedException(Exception):
    pass


class ReporterProxy(object):
    local_ip = None
    browser_mob_server = None

    @staticmethod
    def get_ip():
        binding_server_mode = Shield34Properties.binding_server_mode
        if binding_server_mode == 'local':
            ReporterProxy.local_ip = "127.0.0.1"
        elif binding_server_mode == 'remote':
            if ReporterProxy.local_ip is None:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                try:
                    # doesn't even have to be reachable
                    s.connect(('10.255.255.255', 1))
                    IP = s.getsockname()[0]
                except:
                    try:
                        IP = socket.gethostbyname(socket.gethostname())
                    except:
                        IP = '127.0.0.1'
                finally:
                    s.close()
                ReporterProxy.local_ip = IP
        return ReporterProxy.local_ip

    @staticmethod
    def browser_mob_proxy_is_listening(browser_mob_server, retry_count=60):
        count = 0
        while not browser_mob_server._is_listening():
            time.sleep(0.5)
            count += 1
            if count == retry_count:
                return False
        return True

    @staticmethod
    def start_proxy_management_server():
        if SdkAuthentication.is_authorized():
            from shield34_reporter.container.run_report_container import RunReportContainer
            block_run_report_container = RunReportContainer.get_current_block_run_holder()
            if Shield34Properties.binding_server_mode == 'local':
                if ReporterProxy.browser_mob_server is None:
                    block_run_report_container.proxyServers = []
                    ReporterProxy.browser_mob_server = proxy.get_browsermob_proxy_server()
                    if ReporterProxy.browser_mob_server is None:
                        raise ProxyManagementServerNotInitializedException

            if len(block_run_report_container.proxyServers) == 0:
                proxy_server_instance = get_reporter_proxy()
                if proxy_server_instance is None:
                    return False
                Shield34Logger.logger.console("Created Shield34 reporter proxy")
                block_run_report_container.proxyServers.append(proxy_server_instance)
            return True
        return False

    @staticmethod
    def get_os_proxies():
        if Shield34Properties.selenium_proxy_address is not None:
            return Shield34Properties.selenium_proxy_address

        if sys.version_info > (3, 0):
            proxies = urllib.request.getproxies()
        else:
            proxies = urllib.getproxies()

        if 'https' in proxies:
            proxy = proxies['https']
            proxy = proxy.replace("https://", "")
            return proxy
        elif 'http' in proxies:
            proxy = proxies['http']
            proxy = proxy.replace("http://", "")
            return proxy
        else:
            return None


def create_new_proxy_instance(upstream_chained_proxy=None):
    sub_instance_port = NetworkUtils.get_random_port(ReporterProxy.get_ip())
    if upstream_chained_proxy is not None:
        proxy = ReporterProxy.browser_mob_server.create_proxy(
            params={"trustAllServers": "true", "port": sub_instance_port,
                    "bindAddress": ReporterProxy.get_ip(), 'httpProxy': upstream_chained_proxy})
        Shield34Logger.logger.console(
            "\nStarting new Shield34 Proxy instance on port {} through proxy {}".format(sub_instance_port,
                                                                                        upstream_chained_proxy))
    else:
        proxy = ReporterProxy.browser_mob_server.create_proxy(
            params={"trustAllServers": "true", "port": sub_instance_port,
                    "bindAddress": ReporterProxy.get_ip()})
        Shield34Logger.logger.console("\nStarting new Shield34 Proxy instance on port {}".format(sub_instance_port))

    proxy.base_server = ReporterProxy.browser_mob_server
    create_new_har(proxy)

    return proxy


def create_proxy_params(host):
    upstream_chained_proxy = ReporterProxy.get_os_proxies()
    sub_instance_port = NetworkUtils.get_random_port(host)
    params = {"trustAllServers": "true", "port": sub_instance_port, "bindAddress": host}
    if upstream_chained_proxy is not None:
        params["httpProxy"] = upstream_chained_proxy
    return params


def get_reporter_proxy():
    proxy_client = None
    if Shield34Properties.binding_server_mode == 'local':
        proxy_client = get_local_proxy()

    if Shield34Properties.binding_server_mode == 'remote':
        proxy_client = get_remote_proxy()
    if proxy_client is not None:
        create_new_har(proxy_client)
    return proxy_client


def get_local_proxy():
    proxy_server = proxy.get_browsermob_proxy_server()
    host = get_local_ip()
    if proxy_server is not None:
        return proxy_server.create_proxy(create_proxy_params(host))
    return None


def get_remote_proxy():
    if Shield34Properties.reporter_proxy_address is not None:
        url_parts = Shield34Properties.reporter_proxy_address.split(":")
        port = 80
        if len(url_parts) == 2:
            port = url_parts[1]
        host = url_parts[0]
        proxy_server = proxy.browsermobproxy.RemoteServer(host, int(port))
        if proxy_server is not None:
            return proxy_server.create_proxy(create_proxy_params(host))
    return None


def create_new_har(proxy):
    har_options = {'captureHeaders': True, 'captureContent': True, 'captureCookies': True,
               'captureBinaryContent': True, 'initialPageRef': True, 'initialPageTitle': True}

    if Shield34Properties.send_data_policy == 'strict':
        har_options = {'captureHeaders': True, 'captureContent': False, 'captureCookies': False,
                   'captureBinaryContent': False, 'initialPageRef': True, 'initialPageTitle': True}

    if Shield34Properties.send_data_policy == 'none':
        har_options = {'captureHeaders': False, 'captureContent': False, 'captureCookies': False,
                   'captureBinaryContent': False, 'initialPageRef': False, 'initialPageTitle': False}

    proxy.new_har("shield34.com", options=har_options)
