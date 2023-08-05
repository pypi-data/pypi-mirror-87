import json

import urllib3
from shield34_reporter import requests

from shield34_reporter.consts.shield34_properties import Shield34Properties
from shield34_reporter.exceptions import Shield34LoginFailedException, Shield34ProxyAuthenticationFailedException
from shield34_reporter.model.contracts.sdk_auth_credentials import SdkCredentials

from shield34_reporter.utils.external_proxy import get_external_proxies
from shield34_reporter.utils.logger import Shield34Logger


class SdkAuthentication():

    isAuthorized = False
    userToken = ''


    @staticmethod
    def login():
        try:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            Shield34Properties.initialize()
            sdkAuthCredentials = SdkCredentials(Shield34Properties.api_key, Shield34Properties.api_secret, "")
            payload = json.dumps(sdkAuthCredentials .__dict__)
            headers = {'content-type': 'application/json'}
            code = SdkAuthentication.do_login(payload,headers)
            if code == 407:
                raise Shield34ProxyAuthenticationFailedException
            if code != 200:
                Shield34Logger.logger.info("Login to Shield34 returned code {}".format(code))
                raise Shield34LoginFailedException
        except Exception as e:
            Shield34Logger.logger.info("Login to Shield34 failed with error {}".format(str(e)))
            raise Shield34LoginFailedException

    @staticmethod
    def do_login(payload,headers):
        login_request = requests.post(Shield34Properties.api_base_url + '/auth/project-login', data=payload,
                                      headers=headers, verify=Shield34Properties.enable_ssl_certificate_verification,
                                      proxies=get_external_proxies(), timeout=30)
        if login_request.status_code == 200:
            SdkAuthentication.isAuthorized = True
            response_as_json = login_request.json()
            SdkAuthentication.userToken = response_as_json['data']['token']
        return login_request.status_code

    @staticmethod
    def is_authorized():
        return SdkAuthentication.isAuthorized

    @staticmethod
    def get_user_token():
        return SdkAuthentication.userToken