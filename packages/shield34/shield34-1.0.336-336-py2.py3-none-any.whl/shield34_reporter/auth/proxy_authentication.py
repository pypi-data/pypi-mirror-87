import importlib

from requests.auth import AuthBase
from shield34_reporter.utils import import_utils


def get_authenticator(scheme):
    if scheme in ( 'NTLM'):
        return import_utils.import_module('ntlm_proxy_authentication',__name__,['pywin32'])
    if scheme is not None and scheme.startswith('Basic'):
        return import_utils.import_module('basic_proxy_authentication', __name__, [])
    if scheme in ('Negotiate','Kerberos'):
        return import_utils.import_module('kerberos_proxy_authentication', __name__, ['winkerberos'])
    return None


class ProxyAuthentication(AuthBase):
    def __init__(self,domain=None,username=None, password=None):
        self.domain = domain
        self.username = username
        self.password = password

    def __call__(self, r):
        r.headers['Connection'] = 'Keep-Alive'
        r.register_hook('response', self._response_hook)
        return r

    def _response_hook(self, r, **kwargs):
        if r.status_code != 407:
            return r
        auth_module = get_authenticator(r.headers.get('Proxy-Authenticate', ''))
        if auth_module is not None:
            return auth_module.authenticate_proxy(self, r, **kwargs)
        else:
            return r


