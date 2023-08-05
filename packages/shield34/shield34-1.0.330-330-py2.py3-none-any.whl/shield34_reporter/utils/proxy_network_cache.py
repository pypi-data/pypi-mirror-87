import json
import os
import re

from shield34_reporter.consts.shield34_properties import Shield34Properties
from shield34_reporter.model.csv_rows.debug_exception_log_csv_row import DebugExceptionLogCsvRow
from shield34_reporter.utils.time_utils import TimeUtils


class ProxyNetworkCache:
    __the_cache = None

    def __init__(self, client):
        self.client = client
        self.client.new_har("shield34.com",
                            options={'captureHeaders': True, 'captureContent': True, 'captureCookies': True,
                                     'captureBinaryContent': True, 'initialPageRef': True, 'initialPageTitle': True})
        self.files_to_compress = []

    def replace_har(self, name, options, path_to_save_files):
        browser_network_data = []

        for entry in self.client.har['log']['entries']:
            browser_network_data.append(entry)
        self.client.new_har(name, options=options)

        files = ProxyNetworkCache.write_browser_network_data_to_files(browser_network_data, path_to_save_files, len(self.files_to_compress))
        for f in files:
            self.files_to_compress.append(f)

        return self.files_to_compress

    @staticmethod
    def get_cache(proxy):
        if ProxyNetworkCache.__the_cache is None:
            ProxyNetworkCache.__the_cache = ProxyNetworkCache(proxy)
        return ProxyNetworkCache.__the_cache

    @staticmethod
    def write_browser_network_data_to_files(browser_network_data, path_to_save_files, file_index = 0):
        from shield34_reporter.container.run_report_container import RunReportContainer
        files_to_compress = []
        converted_browser_network_data = ProxyNetworkCache.convert_har_to_browser_network(browser_network_data)
        pattern = None
        if Shield34Properties.filter_network_regexp is not None:
            pattern = re.compile(Shield34Properties.filter_network_regexp)

        for idx, browser_network in enumerate(converted_browser_network_data):
            try:
                if pattern is not None and pattern.search(browser_network['request']['url']) is None:
                    epoch_time = TimeUtils.get_timestamp_from_datetime_str(browser_network['startedDateTime'])
                    file_name = str(file_index) + "_" + str(epoch_time) + ".txt"
                    file_path = os.path.join(path_to_save_files, file_name)
                    if not os.path.exists(path_to_save_files):
                        os.makedirs(path_to_save_files)
                    file = open(file_path, "w")
                    file.write(json.dumps(browser_network))
                    file.close()
                    files_to_compress.append(file)
                    file_index = file_index + 1
            except Exception as e:
                RunReportContainer.add_report_csv_row(
                    DebugExceptionLogCsvRow("Couldn't write browser network data to file!", e))

        return files_to_compress

    @staticmethod
    def convert_har_to_browser_network(browser_network_data):
        from shield34_reporter.container.run_report_container import RunReportContainer
        browser_network_converted_data = []
        for browser_network in browser_network_data:
            try:
                browser_network_request_cookies = []

                if browser_network['request'].get('cookies', None) is not None:
                    for cookie in browser_network['request']['cookies']:
                        browser_network_request_cookies.append({'name': cookie['name'], 'value': cookie['value']})

                browser_network_request_headers = []
                if browser_network['request'].get('headers', None) is not None:
                    for header in browser_network['request']['headers']:
                        browser_network_request_headers.append({'name': header['name'], 'value': header['value']})

                browser_network_request_query_string = []
                if browser_network['request'].get('queryString', None) is not None:
                    for query_string in browser_network['request']['queryString']:
                        browser_network_request_query_string.append(
                            {'name': query_string['name'], 'value': query_string['value']})

                browser_network_request_post_data = {}
                if browser_network['request'].get('postData', None) is not None:

                    browser_network_request_post_data_params = []
                    if browser_network['request']['postData'].get('params', None) is not None:
                        for param in browser_network['request']['postData']['params']:
                            browser_network_request_post_data_params.append(
                                {'name': param['name'], 'value': param['value']})
                    browser_network_request_post_data_text = browser_network['request']['postData'].get('text', '')
                    browser_network_request_post_data = {'mimeType': browser_network['request']['postData']['mimeType'],
                                                         'params': browser_network_request_post_data_params,
                                                         'text': browser_network_request_post_data_text}

                browser_network_request = {
                    'method': browser_network['request']['method'],
                    'url': browser_network['request']['url'],
                    'httpVersion': browser_network['request']['httpVersion'],
                    'cookies': browser_network_request_cookies,
                    'headers': browser_network_request_headers,
                    'queryString': browser_network_request_query_string,
                    'postRequestData': browser_network_request_post_data,
                    'headersSize': browser_network['request']['headersSize'],
                    'bodySize': browser_network['request']['bodySize']
                }

                browser_network_response_cookies = []

                if browser_network['response'].get('cookies', None) is not None:
                    for cookie in browser_network['response']['cookies']:
                        # cookie_name = browser_network['response']['cookies'].get('name', None) if browser_network['response']['cookies'].get('name', None) is not None else ''
                        cookie_path = cookie.get('path', None) if cookie.get('path', None) is not None else ''
                        cookie_expires = cookie.get('expires', None) if cookie.get('expires', None) is not None else ''
                        cookie_http_only = cookie.get('httpOnly', None) if cookie.get('httpOnly',
                                                                                      None) is not None else ''
                        cookie_secure = cookie.get('secure', None) if cookie.get('secure', None) is not None else ''
                        browser_network_response_cookies.append({'name': cookie['name'],
                                                                 'value': cookie['value'],
                                                                 'path': cookie_path,
                                                                 'expires': cookie_expires,
                                                                 'httpOnly': cookie_http_only,
                                                                 'secure': cookie_secure})

                browser_network_response_headers = []
                if browser_network['response'].get('headers', None) is not None:
                    for header in browser_network['response']['headers']:
                        browser_network_response_headers.append({'name': header['name'], 'value': header['value']})

                if browser_network['response']['content'].get('encoding', None) is None:
                    response_content_encoding = ''
                else:
                    response_content_encoding = browser_network['response']['content']['encoding']
                if browser_network['response']['content'].get('text', None) is None:
                    response_content_text = ''
                else:
                    response_content_text = browser_network['response']['content']['text']
                browser_network_response_content = {'size': browser_network['response']['content']['size'],
                                                    'mimeType': browser_network['response']['content']['mimeType'],
                                                    'text': response_content_text,
                                                    'encoding': response_content_encoding}

                browser_network_response = {'status': browser_network['response']['status'],
                                            'statusText': browser_network['response']['statusText'],
                                            'httpVersion': browser_network['response']['httpVersion'],
                                            'cookies': browser_network_response_cookies,
                                            'headers': browser_network_response_headers,
                                            'content': browser_network_response_content,
                                            'redirectURL': browser_network['response']['redirectURL'],
                                            'headersSize': browser_network['response']['headersSize'],
                                            'bodySize': browser_network['response']['bodySize'],
                                            }

                browser_network_timings = {
                    'blockedNanos': browser_network['timings']['blocked'],
                    'dnsNanos': browser_network['timings']['dns'],
                    'connectNanos': browser_network['timings']['connect'],
                    'sendNanos': browser_network['timings']['send'],
                    'waitNanos': browser_network['timings']['wait'],
                    'receiveNanos': browser_network['timings']['receive'],
                    'sslNanos': browser_network['timings']['ssl'],

                }

                browser_network_new_json = {
                    'pageref': browser_network['pageref'],
                    'startedDateTime': browser_network['startedDateTime'],
                    'request': browser_network_request,
                    'response': browser_network_response,
                    'serverIPAddress': browser_network.get('serverIPAddress', ''),
                    'timings': browser_network_timings
                }
                browser_network_converted_data.append(browser_network_new_json)
            except Exception as e:
                RunReportContainer.add_report_csv_row(
                    DebugExceptionLogCsvRow("Couldn't retrieve browser network data", e))

        return browser_network_converted_data