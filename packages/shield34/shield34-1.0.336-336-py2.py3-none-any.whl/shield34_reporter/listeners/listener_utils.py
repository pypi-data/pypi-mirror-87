import json
import os
import re
import shutil
import sys
import time

from shield34_reporter import requests
from shield34_reporter.auth.sdk_authentication import SdkAuthentication
from shield34_reporter.consts.shield34_properties import Shield34Properties
from shield34_reporter.model.contracts import block_contract as bc
from shield34_reporter.model.contracts import run_contract as rc
from shield34_reporter.model.contracts.block_run_contract import BlockRunContract
from shield34_reporter.model.contracts.run_contract import RunContract
from shield34_reporter.model.contracts.s3.s3_file_details import TarGzS3FileDetails, BrowserNetworkS3FileDetails
from shield34_reporter.model.contracts.s3_file_details import S3FileDetails
from shield34_reporter.model.csv_rows.browser_network_data_csv_row import BrowserNetworkDataCsvRow
from shield34_reporter.model.csv_rows.debug_exception_log_csv_row import DebugExceptionLogCsvRow
from shield34_reporter.model.enums.file_type import FileType
from shield34_reporter.model.enums.status import Status
from shield34_reporter.utils import file_handler
from shield34_reporter.utils.aws_utils import AwsUtils
from shield34_reporter.utils.browser_console_logs_helper import BrowserConsoleLogsHelper
from shield34_reporter.utils.csv_file_handler import CsvFileHandler
from shield34_reporter.utils.driver_utils import DriverUtils
from shield34_reporter.utils.external_proxy import get_external_proxies
from shield34_reporter.utils.logger import Shield34Logger
from shield34_reporter.utils.pabot_parallel_runs import PabotParallelRuns
from shield34_reporter.utils.tar_file_handler import TarFileHandler
from shield34_reporter.utils.time_utils import TimeUtils
from shield34_reporter.listeners import enum_encoder


class ListenerUtils():

    @staticmethod
    def save_or_update_run(run_contract):
        if SdkAuthentication.isAuthorized:
            payload = json.dumps(run_contract.__dict__)
            command_line = str(sys.argv)
            if command_line.find("PABOT") > -1 or command_line.find("pabot") > -1:
                try :
                    pabot_instance = PabotParallelRuns()
                    pabot_instance.acquire_lock("shield34_create_run")
                    if pabot_instance.check_if_key_is_shared("shield34_run_id"):
                        run_contract = pabot_instance.get_existing_run()
                        pabot_instance.release_lock("shield34_create_run")
                        return run_contract
                    else:
                        run_contract = ListenerUtils.internal_save_or_update_run(payload)
                        if run_contract is None:
                            run_contract = RunContract()
                            pabot_instance.set_run(run_contract)
                            pabot_instance.release_lock("shield34_create_run")
                            return run_contract
                        else:
                            pabot_instance.set_run(run_contract)
                            pabot_instance.release_lock("shield34_create_run")
                            return run_contract
                    pabot_instance.release_lock("shield34_create_run")
                except Exception as e:
                    pabot_instance.release_lock("shield34_create_run")
                    Shield34Logger.logger.console(
                        "Please make sure to use the flag --pabotlib to run the tests using Shield34 listener, for example: pabot --pabotlib --listener shield34_reporter.listeners.robot_listener.RobotListener")
                    Shield34Logger.logger.console(str(e))
                    raise e
            else:
                run_contract = ListenerUtils.internal_save_or_update_run(payload)
                if run_contract is None:
                    return RunContract()
                else:
                    return run_contract
        return RunContract()

    @staticmethod
    def internal_save_or_update_run(payload):
        headers = {'content-type': 'application/json',
                   'Authorization': 'Shield34-Project ' + SdkAuthentication.get_user_token()}
        request = requests.post(Shield34Properties.api_base_url + '/report/save-run', data=payload,
                                headers=headers, verify=Shield34Properties.enable_ssl_certificate_verification, proxies=get_external_proxies())
        if request.status_code == 200:
            content_as_json = request.json()
            return rc.from_dict(content_as_json['data'])
        else:
            return None

    @staticmethod
    def save_or_update_block_run(block_run_contract):
        if SdkAuthentication.isAuthorized:
            payload = json.dumps(block_run_contract.__dict__)
            headers = {'content-type': 'application/json', 'Authorization': 'Shield34-Project ' + SdkAuthentication.get_user_token()}
            request = requests.post(Shield34Properties.api_base_url + '/report/save-block-run', data=payload,
                                    headers=headers, verify=Shield34Properties.enable_ssl_certificate_verification, proxies=get_external_proxies())
            if request.status_code == 200:
                content_as_json = request.json()
                status = content_as_json['data']['status']
                start_timestamp = content_as_json['data']['startTimestamp']
                end_timestamp = content_as_json['data']['endTimestamp']
                report_file_path = content_as_json['data']['reportFilePath']
                browser_details = content_as_json['data']['browserDetails']
                window_resolution = content_as_json['data']['windowResolution']
                driver_details = content_as_json['data']['driverDetails']
                os_type = content_as_json['data']['osType']
                block_contract = bc.from_dict(content_as_json['data']['blockContract'])
                run_contract = rc.from_dict(content_as_json['data']['runContract'])
                id = content_as_json['data']['id']
                return BlockRunContract(status, start_timestamp, end_timestamp, report_file_path, browser_details, window_resolution, driver_details, os_type, block_contract, run_contract, id)

        return BlockRunContract()


    @staticmethod
    def save_report(report_path, report_output_path, block_run_contract):
        from shield34_reporter.container.run_report_container import RunReportContainer
        CsvFileHandler.write_csv_file(os.path.join(report_path, 'report.csv'), RunReportContainer.get_current_block_run_holder().blockReport, ["timestamp", "row_sub_type", "row_type",  "row_value"])
        general_report = []
        general_report.append(RunReportContainer.get_current_block_run_holder().generalReport)
        CsvFileHandler.write_csv_file(os.path.join(report_path, 'general.csv'), general_report, ["timestamp", "run_id", "block_id", "parent_suite_name", "run_start_timestamp", "test_start_timestamp", "suite_name", "test_class_name", "test_name" "test_params"])
        if block_run_contract.status == Status.PASSED:
            file_handler.write_data_to_json_file(report_path, 'webelement_locators_descriptor.json', RunReportContainer.get_current_block_run_holder().webElementDescriptors)
            TarFileHandler.make_tarfile(report_output_path, "reports.tar.gz", [os.path.join(report_path, 'report.csv'),
                                                                               os.path.join(report_path, 'general.csv'),
                                                                               os.path.join(report_path,
                                                                                            'webelement_locators_descriptor.json')])
        else:
            TarFileHandler.make_tarfile(report_output_path, "reports.tar.gz", [os.path.join(report_path, 'report.csv'), os.path.join(report_path, 'general.csv')])
        s3_file_details = S3FileDetails(block_run_contract.runContract.id, block_run_contract.id, "reports.tar.gz", FileType.TAG_GZ_FILE)
        tar_gz_s3_file_details = TarGzS3FileDetails(block_run_contract.runContract.id, block_run_contract.id, "reports.tar.gz")
        pre_signed_url_contract = AwsUtils.get_tar_gz_upload_to_s3_url(tar_gz_s3_file_details)
        file_uploaded = ListenerUtils.upload_report_to_s3(pre_signed_url_contract, os.path.join(report_path, "reports.tar.gz"))
        if file_uploaded:
            ListenerUtils.save_report_file(s3_file_details)
        shutil.rmtree(report_path)

        # TODO delete tar file.

    @staticmethod
    def upload_report_to_s3(pre_signed_url_contract, report_path):
        if SdkAuthentication.isAuthorized:
            file_object = open(report_path, 'rb')
            http_response = requests.put(pre_signed_url_contract.url,
                                         verify=Shield34Properties.enable_ssl_certificate_verification,
                                         data=file_object.read(), proxies=get_external_proxies())
            file_object.close()
            if http_response.status_code == 200:
                return True

    @staticmethod
    def save_report_file(s3_file_details):
        if SdkAuthentication.isAuthorized:
            payload = json.dumps(s3_file_details.__dict__)
            headers = {'content-type': 'application/json',
                       'Authorization': 'Shield34-Project ' + SdkAuthentication.get_user_token()}
            request = requests.post(Shield34Properties.api_base_url + '/report/save-report', data=payload,
                                    headers=headers, verify=Shield34Properties.enable_ssl_certificate_verification, proxies=get_external_proxies())

    @staticmethod
    def get_test_run_url(current_block_run):
        if SdkAuthentication.isAuthorized:
            payload = json.dumps(current_block_run.__dict__)
            headers = {'content-type': 'application/json', 'Authorization': 'Shield34-Project ' + SdkAuthentication.get_user_token()}
            request = requests.post(Shield34Properties.api_base_url + '/report/get-block-run-details', data=payload,
                                    headers=headers, verify=Shield34Properties.enable_ssl_certificate_verification, proxies=get_external_proxies())
            if request.status_code == 200:
                content_as_json = request.json()
                app_path = content_as_json['data']['appPath']
                return app_path
            else:
                return "N/A"


    @staticmethod
    def fetch_browser_logs():
        from shield34_reporter.container.run_report_container import RunReportContainer
        driver = DriverUtils.get_current_driver()
        driver_not_closed = RunReportContainer.driver_counter > 0
        if driver is not None and driver_not_closed:
            try:
                try:
                    browser_logs = RunReportContainer.get_current_block_run_holder().browser_logs
                    RunReportContainer.get_current_block_run_holder().browser_logs = None
                except AttributeError:
                    browser_logs = None
                logs = driver.get_log('browser') if browser_logs is None else browser_logs
                for logEntry in logs:
                    BrowserConsoleLogsHelper.add_browser_logs_to_report(logEntry)
            except Exception as e:
                RunReportContainer.add_report_csv_row(DebugExceptionLogCsvRow("Couldn't retrieve logs from driver", e))

    @staticmethod
    def get_file_path(f):
        return os.path.realpath(f.name)




    @staticmethod
    def fetch_browser_network2():
        try:
            if Shield34Properties.send_data_policy == 'none':
                return
            Shield34Logger.logger.info("\r\nPreparing to upload all browser network traffic to Shield34 servers.")
            files_to_compress = ListenerUtils.write_all_network_data_to_files()
            Shield34Logger.logger.info("Captured " + str(len(files_to_compress)) + " files from browser network")
            from shield34_reporter.container.run_report_container import RunReportContainer
            path_to_save_files = os.path.join(
                RunReportContainer.get_current_block_run_holder().get_current_test_folder(), 'har_files')
            if len(files_to_compress) != 0:
                current_time = str(int(round(time.time() * 1000.)))
                from random import seed, random
                file_name_to_save = "browser_network{}-{}.tar.gz".format(current_time, random())

                files_to_compress_save = [os.path.realpath(f.name) for f in files_to_compress]
                TarFileHandler.make_tarfile(path_to_save_files, file_name_to_save, files_to_compress_save)

                block_run_contract = RunReportContainer.get_current_block_run_holder().blockRunContract
                browser_network_s3_file_details = BrowserNetworkS3FileDetails(
                    block_run_contract.runContract.id, block_run_contract.id,
                    file_name_to_save)

                pre_signed_url_contract = AwsUtils.get_browser_network_upload_to_s3_url(
                    browser_network_s3_file_details)
                Shield34Logger.logger.info("Starting to upload network data to Shield34 servers")
                file_uploaded = ListenerUtils.upload_report_to_s3(pre_signed_url_contract,
                                                                  os.path.join(path_to_save_files,
                                                                               file_name_to_save))
                if file_uploaded:
                    RunReportContainer.add_report_csv_row(
                        BrowserNetworkDataCsvRow(pre_signed_url_contract.fileName, file_name_to_save))

        except Exception as e:
            Shield34Logger.logger.warn("Failed to upload network data" + str(e))


    @staticmethod
    def fetch_browser_network():
        try:
            Shield34Logger.logger.info("\r\nPreparing to upload browser network traffic to Shield34 servers.")
            from shield34_reporter.container.run_report_container import RunReportContainer
            browser_network_data = []
            for i in range(0,len(RunReportContainer.get_current_block_run_holder().proxyServers)):
                proxyServer  = RunReportContainer.get_current_block_run_holder().proxyServers[i]
                if proxyServer is not None:
                    for entry in proxyServer.har['log']['entries']:
                        browser_network_data.append(entry)
            Shield34Logger.logger.info("Captured "+str(len(browser_network_data))+" files from browser network")
            if len(browser_network_data) > 0:
                path_to_save_files = os.path.join(RunReportContainer.get_current_block_run_holder().get_current_test_folder(),  'har_files')
                files_to_compress = ListenerUtils.write_browser_network_data_to_files(browser_network_data, path_to_save_files)

                Shield34Logger.logger.info("After filtering static resources compressing " + str(len(files_to_compress)) + " network files ")
                if len(files_to_compress) != 0:
                    current_time = str(int(round(time.time() * 1000.)))
                    from random import seed, random
                    file_name_to_save = "browser_network{}-{}.tar.gz".format(current_time,random())

                    files_to_compress_save = [os.path.realpath(f.name) for f in files_to_compress];
                    TarFileHandler.make_tarfile(path_to_save_files, file_name_to_save, files_to_compress_save)

                    block_run_contract = RunReportContainer.get_current_block_run_holder().blockRunContract
                    browser_network_s3_file_details = BrowserNetworkS3FileDetails(
                        block_run_contract.runContract.id, block_run_contract.id,
                        file_name_to_save)

                    pre_signed_url_contract = AwsUtils.get_browser_network_upload_to_s3_url(browser_network_s3_file_details)
                    Shield34Logger.logger.info("Starting to upload network data to Shield34 servers")
                    file_uploaded = ListenerUtils.upload_report_to_s3(pre_signed_url_contract,
                                                                      os.path.join(path_to_save_files, file_name_to_save))
                    if file_uploaded:
                        RunReportContainer.add_report_csv_row(BrowserNetworkDataCsvRow(pre_signed_url_contract.fileName, file_name_to_save))

        except Exception as e:
            Shield34Logger.logger.warn("Failed to upload network data"+str(e))

    @staticmethod
    def write_browser_network_entry_to_files( browser_network,file_index, path_to_save_files):
        pattern = None

        if Shield34Properties.filter_network_regexp is not None and Shield34Properties.filter_network_regexp != '':
            pattern = re.compile(Shield34Properties.filter_network_regexp)
        try:
            if pattern is None or pattern.search(browser_network['request']['url']) is None:
                epoch_time = TimeUtils.get_timestamp_from_datetime_str(browser_network['startedDateTime'])
                file_name = str(file_index) + "_" + str(epoch_time) + ".txt"
                file_path = os.path.join(path_to_save_files, file_name)
                if not os.path.exists(path_to_save_files):
                    os.makedirs(path_to_save_files)
                file = open(file_path, "w")
                file.write(json.dumps(browser_network))
                file.close()
                return file

        except Exception as e:
            from shield34_reporter.container.run_report_container import RunReportContainer
            RunReportContainer.add_report_csv_row(
                DebugExceptionLogCsvRow("Couldn't write browser network data to file!", e))
            return None

    @staticmethod
    def write_browser_network_data_to_files(browser_network_data, path_to_save_files):
        from shield34_reporter.container.run_report_container import RunReportContainer
        files_to_compress = []
        file_index = 0
        converted_browser_network_data = ListenerUtils.convert_har_to_browser_network(browser_network_data)
        for idx, browser_network in enumerate(converted_browser_network_data):
            saved_file = ListenerUtils.write_browser_network_entry_to_files(browser_network,file_index,path_to_save_files)
            if saved_file is not None:
                file_index = file_index + 1
                files_to_compress.append(saved_file)
        Shield34Logger.logger.console("Compressed {} files of network traffic".format( file_index))
        return files_to_compress


    @staticmethod
    def convert_har_entry_to_browser_network(browser_network):
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
                    cookie_http_only = cookie.get('httpOnly', None) if cookie.get('httpOnly', None) is not None else ''
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
            return browser_network_new_json
        except Exception as e:
            from shield34_reporter.container.run_report_container import RunReportContainer
            RunReportContainer.add_report_csv_row(DebugExceptionLogCsvRow("Couldn't retrieve browser network data", e))
            return None

    @staticmethod
    def convert_har_to_browser_network(browser_network_data):
        from shield34_reporter.container.run_report_container import RunReportContainer
        browser_network_converted_data = []
        for browser_network in browser_network_data:
            converted_browser_data = ListenerUtils.convert_har_entry_to_browser_network(browser_network)
            if converted_browser_data is not None:
                browser_network_converted_data.append(converted_browser_data)

        return browser_network_converted_data

    @staticmethod
    def str_to_class(str):
        return getattr(sys.modules[__name__], str)


    @staticmethod
    def write_all_network_data_to_files():
        files_to_compress = []
        file_index = 0
        from shield34_reporter.container.run_report_container import RunReportContainer
        path_to_save_files = os.path.join(
            RunReportContainer.get_current_block_run_holder().get_current_test_folder(), 'har_files')

        for i in range(0, len(RunReportContainer.get_current_block_run_holder().proxyServers)):
            proxy_server = RunReportContainer.get_current_block_run_holder().proxyServers[i]
            for entry in proxy_server.har['log']['entries']:
                try:
                    converted_browser_data  = ListenerUtils.convert_har_entry_to_browser_network(entry)
                    if converted_browser_data is not None:
                        saved_file = ListenerUtils.write_browser_network_entry_to_files(converted_browser_data, file_index, path_to_save_files)
                        if saved_file is not None:
                            file_index = file_index+1
                            files_to_compress.append(saved_file)
                except Exception as e:
                    Shield34Logger.logger.warn("Failed to upload network entry "+str(e))
        return files_to_compress