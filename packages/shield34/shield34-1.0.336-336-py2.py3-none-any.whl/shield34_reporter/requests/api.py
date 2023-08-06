import requests

from shield34_reporter.auth import proxy_authentication
from shield34_reporter.consts.shield34_properties import Shield34Properties
from shield34_reporter.utils.external_proxy import get_external_proxies


def prepare_proxy_authentication(url):
    Shield34Properties.initialize()
    proxy_auth = proxy_authentication.ProxyAuthentication(
        domain=Shield34Properties.external_proxy_domain,
        username=Shield34Properties.external_proxy_username,
        password=Shield34Properties.external_proxy_password

    )
    if url.startswith(Shield34Properties.api_base_url):
        url = url.replace('https://', 'http://')
    return url, proxy_auth



def request(method, url, **kwargs):
    try:
        response = requests.request(method=method,
                                    url=url,
                                    **kwargs)
        if response.status_code == 407:

            url, kwargs['auth'] = prepare_proxy_authentication(url)
            response = requests.request(method=method,
                                        url=url,
                                        **kwargs)

    except Exception as err:
        url, kwargs['auth'] = prepare_proxy_authentication(url)
        response = requests.request(method=method,
                                    url=url,
                                    **kwargs)
    return response


def get(url, params=None, **kwargs):
    try:
        response = requests.get(url=url,
                                params=params,
                                **kwargs)
        if response.status_code == 407:
            url, kwargs['auth'] = prepare_proxy_authentication(url)
            response = requests.get(url=url,
                                    params=params,
                                    **kwargs)
    except Exception as err:
        url, kwargs['auth'] = prepare_proxy_authentication(url)
        response = requests.get(url=url,
                                params=params,
                                **kwargs)
    return response


def post(url, data=None, json=None, **kwargs):
    try:
        response = requests.post(url=url,
                                 data=data,
                                 json=json,
                                 **kwargs)
        if response.status_code == 407:
            url, kwargs['auth'] = prepare_proxy_authentication(url)
            response = requests.post(url=url,
                                     data=data,
                                     json=json,
                                     **kwargs)
    except Exception as err:
        url, kwargs['auth'] = prepare_proxy_authentication(url)
        response = requests.post(url=url,
                                 data=data,
                                 json=json,
                                 **kwargs)
    return response


def options(url, **kwargs):
    try:
        response = requests.options(url, proxies=get_external_proxies(), **kwargs)
        if response.status_code == 407:
            url, kwargs['auth'] = prepare_proxy_authentication(url)
            response = requests.options(url, proxies=get_external_proxies(), **kwargs)
    except Exception as err:
        url, kwargs['auth'] = prepare_proxy_authentication(url)
        response = requests.options(url, proxies=get_external_proxies(), **kwargs)
    return response


def head(url, **kwargs):
    try:
        response = requests.head(url, proxies=get_external_proxies(), **kwargs)
        if response.status_code == 407:
            url, kwargs['auth'] = prepare_proxy_authentication(url)
            response = requests.head(url, proxies=get_external_proxies(), **kwargs)
    except Exception as err:
        url, kwargs['auth'] = prepare_proxy_authentication(url)
        response = requests.head(url, proxies=get_external_proxies(), **kwargs)
    return response


def put(url, data=None, **kwargs):
    try:
        response = requests.put(url=url,
                                data=data,
                                **kwargs)
        if response.status_code == 407:
            url, kwargs['auth'] = prepare_proxy_authentication(url)
            response = requests.put(url=url,
                                    data=data,
                                    **kwargs)
    except Exception as err:
        url, kwargs['auth'] = prepare_proxy_authentication(url)
        response = requests.put(url=url,
                                data=data,
                                **kwargs)
    return response


def patch(url, data=None, **kwargs):
    try:
        response = requests.patch(url, data=data, proxies=get_external_proxies(), **kwargs)
        if response.status_code == 407:
            url, kwargs['auth'] = prepare_proxy_authentication(url)
            response = requests.patch(url, data=data, proxies=get_external_proxies(), **kwargs)
    except Exception as err:
        url, kwargs['auth'] = prepare_proxy_authentication(url)
        response = requests.patch(url, data=data, proxies=get_external_proxies(), **kwargs)
    return response


def delete(url, **kwargs):
    try:
        response = requests.delete(url, proxies=get_external_proxies(), **kwargs)
        if response.status_code == 407:
            url, kwargs['auth'] = prepare_proxy_authentication(url)
            response = requests.delete(url, proxies=get_external_proxies(), **kwargs)
    except Exception as err:
        url, kwargs['auth'] = prepare_proxy_authentication(url)
        response = requests.delete(url, proxies=get_external_proxies(), **kwargs)
    return response


def get_arg(name, default_value, **kwargs):
    if name in kwargs:
        return kwargs.get(name)
    else:
        return default_value
