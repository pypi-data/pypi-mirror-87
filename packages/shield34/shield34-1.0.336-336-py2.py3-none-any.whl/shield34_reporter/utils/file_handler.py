
import json
import os

from shield34_reporter import requests
from shield34_reporter.utils.external_proxy import get_external_proxies


def write_data_to_json_file(json_file_directory, json_file_name, data):
    with open(os.path.join(json_file_directory, json_file_name), 'w') as f:
        json.dump(data, f)


def upload_file(url, file):
    from shield34_reporter.consts.shield34_properties import Shield34Properties
    http_response = requests.put(url, data=file,
                                 verify=Shield34Properties.enable_ssl_certificate_verification,
                                 proxies=get_external_proxies())
    if http_response.status_code == 200:
        return True
    else:
        return False
