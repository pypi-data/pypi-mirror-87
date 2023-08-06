
def get_external_proxies():
    from shield34_reporter.consts.shield34_properties import Shield34Properties
    if Shield34Properties.external_proxy_address is not None and Shield34Properties.external_proxy_address != '':
        proxy_dict = {"http": Shield34Properties.external_proxy_address,
                      "https": Shield34Properties.external_proxy_address}
        return proxy_dict
    return None

