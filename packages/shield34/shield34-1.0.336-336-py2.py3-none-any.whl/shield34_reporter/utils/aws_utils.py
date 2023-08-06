import json

from shield34_reporter import requests
from shield34_reporter.consts.shield34_properties import Shield34Properties
from shield34_reporter.model.contracts.pre_signed_url_contract import PreSignedUrlContract
from shield34_reporter.utils.external_proxy import get_external_proxies


class AwsUtils():

    @staticmethod
    def get_file_upload_to_s3_url(s3_file_details):
        from shield34_reporter.auth.sdk_authentication import SdkAuthentication
        payload = json.dumps(s3_file_details.__dict__)
        headers = {'content-type': 'application/json',
                   'Authorization': 'Shield34-Project ' + SdkAuthentication.get_user_token()}
        request = requests.post(Shield34Properties.api_base_url + '/report/get-presigned-upload-url', data=payload,
                                headers=headers, verify=Shield34Properties.enable_ssl_certificate_verification,
                                proxies=get_external_proxies())
        if request.status_code == 200:
            content_as_json = request.json()
            pre_signed_url = PreSignedUrlContract(content_as_json['data']['url'], content_as_json['data']['timestamp'], content_as_json['data']['fileName'])
            return pre_signed_url
        return ""

    @staticmethod
    def get_screenshot_upload_to_s3_url(screen_shot_s3_file_details):
        from shield34_reporter.auth.sdk_authentication import SdkAuthentication
        payload = json.dumps(screen_shot_s3_file_details.__dict__)
        headers = {'content-type': 'application/json',
                   'Authorization': 'Shield34-Project ' + SdkAuthentication.get_user_token()}
        request = requests.post(Shield34Properties.api_base_url + '/report/get-screenshot-presigned-upload-url',
                                data=payload,
                                headers=headers, verify=Shield34Properties.enable_ssl_certificate_verification,
                                proxies=get_external_proxies())
        if request.status_code == 200:
            content_as_json = request.json()
            pre_signed_url = PreSignedUrlContract(content_as_json['data']['url'], content_as_json['data']['timestamp'],
                                                  content_as_json['data']['fileName'])
            return pre_signed_url
        return ""

    @staticmethod
    def get_browser_network_upload_to_s3_url(browser_network_s3_file_details):
        from shield34_reporter.auth.sdk_authentication import SdkAuthentication
        payload = json.dumps(browser_network_s3_file_details.__dict__)
        headers = {'content-type': 'application/json',
                   'Authorization': 'Shield34-Project ' + SdkAuthentication.get_user_token()}
        request = requests.post(Shield34Properties.api_base_url + '/report/get-browser-network-data-presigned-upload-url',
                                data=payload,
                                headers=headers, verify=Shield34Properties.enable_ssl_certificate_verification,
                                proxies=get_external_proxies())
        if request.status_code == 200:
            content_as_json = request.json()
            pre_signed_url = PreSignedUrlContract(content_as_json['data']['url'], content_as_json['data']['timestamp'],
                                                  content_as_json['data']['fileName'])
            return pre_signed_url
        return ""

    @staticmethod
    def get_tar_gz_upload_to_s3_url(tar_gz_s3_file_details):
        from shield34_reporter.auth.sdk_authentication import SdkAuthentication
        payload = json.dumps(tar_gz_s3_file_details.__dict__)
        headers = {'content-type': 'application/json',
                   'Authorization': 'Shield34-Project ' + SdkAuthentication.get_user_token()}
        request = requests.post(Shield34Properties.api_base_url + '/report/get-tar-gz-presigned-upload-url', data=payload,
                                headers=headers, verify=Shield34Properties.enable_ssl_certificate_verification,
                                proxies=get_external_proxies())
        if request.status_code == 200:
            content_as_json = request.json()
            pre_signed_url = PreSignedUrlContract(content_as_json['data']['url'], content_as_json['data']['timestamp'],
                                                  content_as_json['data']['fileName'])
            return pre_signed_url
        return ""

    @staticmethod
    def get_browser_network_upload_to_s3_url(browser_network_s3_file_details):
        from shield34_reporter.auth.sdk_authentication import SdkAuthentication
        payload = json.dumps(browser_network_s3_file_details.__dict__)
        headers = {'content-type': 'application/json',
                   'Authorization': 'Shield34-Project ' + SdkAuthentication.get_user_token()}
        request = requests.post(Shield34Properties.api_base_url + '/report/get-browser-network-data-presigned-upload-url',
                                data=payload,
                                headers=headers, verify=Shield34Properties.enable_ssl_certificate_verification,
                                proxies=get_external_proxies())
        if request.status_code == 200:
            content_as_json = request.json()
            pre_signed_url = PreSignedUrlContract(content_as_json['data']['url'], content_as_json['data']['timestamp'],
                                                  content_as_json['data']['fileName'])
            return pre_signed_url
        return ""

    @staticmethod
    def get_screenshot_upload_to_s3_url(screenshot_s3_file_details):
        from shield34_reporter.auth.sdk_authentication import SdkAuthentication
        payload = json.dumps(screenshot_s3_file_details.__dict__)
        headers = {'content-type': 'application/json',
                   'Authorization': 'Shield34-Project ' + SdkAuthentication.get_user_token()}
        request = requests.post(
            Shield34Properties.api_base_url + '/report/get-screenshot-presigned-upload-url',
            data=payload,
            headers=headers, verify=Shield34Properties.enable_ssl_certificate_verification, proxies=get_external_proxies())
        if request.status_code == 200:
            content_as_json = request.json()
            pre_signed_url = PreSignedUrlContract(content_as_json['data']['url'], content_as_json['data']['timestamp'],
                                                  content_as_json['data']['fileName'])
            return pre_signed_url
        return ""
