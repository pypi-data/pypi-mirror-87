import configparser
import fnmatch
import os

from shield34_reporter.consts.shield34_properties_constants import Shield34PropertiesConstants
from shield34_reporter.exceptions import Shield34PropertiesFileNotFoundException, Shield34PropertiesSyntaxIncorrect


class Shield34Properties:
    DEFAULT_API_BASE_URL = 'https://reports-api.shield34.com'
    HTTP_API_BASE_URL = 'http://reports-api.shield34.com'
    isInitialized = False
    configParser = configparser.ConfigParser()
    api_key = None
    api_secret = None
    binding_server_mode = None
    api_base_url = DEFAULT_API_BASE_URL
    http_base_url = HTTP_API_BASE_URL
    external_proxy_address = None
    external_proxy_domain = None
    external_proxy_username = None
    external_proxy_password = None
    propertiesFilePath = None
    enable_ssl_certificate_verification=True
    selenium_proxy_address=None
    reporter_proxy_address = None
    filter_network_regexp = None
    http_library = "requests"
    #all - send all data
    #strict - dont send page html
    #none - no data
    send_data_policy = "all"

    @staticmethod
    def get_value(section, key):
        if not Shield34Properties.isInitialized:
            raise Shield34PropertiesSyntaxIncorrect
        return Shield34Properties.configParser.get(section, key)

    @staticmethod
    def getPropertiesFilePath():
        filename = None
        if Shield34Properties.propertiesFilePath is not None:
            if os.path.exists(Shield34Properties.propertiesFilePath) and os.path.isfile(Shield34Properties.propertiesFilePath):
                filename = Shield34Properties.propertiesFilePath

        if filename is None:
            filename = Shield34Properties.findPropertiesFilePath()

        if filename is None:
            raise Shield34PropertiesFileNotFoundException

        return filename

    @staticmethod
    def find_files(directory, pattern):
        for root, dirs, files in os.walk(directory):
            for basename in files:
                if fnmatch.fnmatch(basename, pattern):
                    filename = os.path.join(root, basename)
                    return filename

        return ""

    @staticmethod
    def findPropertiesFilePath():
        path = "."
        filename = ""
        while filename == "":
            filename = Shield34Properties.find_files(path, 'shield34.ini')
            if filename == "":
                new_path = os.path.abspath(os.path.join(path, os.pardir))
                if new_path == path:
                    break
                else:
                    path = new_path
        if filename == "":
            return None
        return filename

    @staticmethod
    def setPropertiesFilePath(filename):
        Shield34Properties.propertiesFilePath = filename

    @staticmethod
    def readPropertiesFile():
        propertiesFilePath = ""
        try:
            propertiesFilePath = Shield34Properties.getPropertiesFilePath()
            if propertiesFilePath != "":
                Shield34Properties.configParser.read(propertiesFilePath)
                Shield34Properties.isInitialized = True
            else:
                raise Shield34PropertiesFileNotFoundException()
        except Shield34PropertiesFileNotFoundException as e:
            raise e

        if propertiesFilePath == "":
            raise Shield34PropertiesFileNotFoundException

    @staticmethod
    def get_section_value(section,key,default_value):
        try:
            return Shield34Properties.get_value(section,key)
        except Exception:
            return default_value


    @staticmethod
    def initialize():
        if not Shield34Properties.isInitialized:
            Shield34Properties.readPropertiesFile()
            Shield34Properties.api_key = Shield34Properties.get_value(
                Shield34PropertiesConstants.PROP_REPORTS_SECTION,
                Shield34PropertiesConstants.PROP_REPORTS_API_KEY)

            Shield34Properties.api_secret = Shield34Properties.get_value(
                Shield34PropertiesConstants.PROP_REPORTS_SECTION,
                Shield34PropertiesConstants.PROP_REPORTS_API_SECRET)

            Shield34Properties.filter_network_regexp = Shield34Properties.get_section_value(
                Shield34PropertiesConstants.PROP_REPORTS_SECTION,
                Shield34PropertiesConstants.PROP_FILTER_NETWORK_REGEXP_KEY,
                r".+\.(js|svg|css|ico|png|jpg|gif)")

            Shield34Properties.send_data_policy = Shield34Properties.get_section_value(
                Shield34PropertiesConstants.PROP_REPORTS_SECTION,
                Shield34PropertiesConstants.PROP_SEND_DATA_POLICY_KEY,
                r"all")

            Shield34Properties.binding_server_mode = Shield34Properties.get_section_value(
                Shield34PropertiesConstants.PROP_PROXY_SECTION,
                Shield34PropertiesConstants.PROP_PROXY_BINDING_MODE,
                "local")

            Shield34Properties.reporter_proxy_address = Shield34Properties.get_section_value(
                Shield34PropertiesConstants.PROP_PROXY_SECTION,
                Shield34PropertiesConstants.PROP_REPORTER_PROXY_ADDRESS,
                "127.0.0.1")

            Shield34Properties.api_base_url = Shield34Properties.get_section_value(
                Shield34PropertiesConstants.PROP_REPORTS_SECTION,
                Shield34PropertiesConstants.PROP_REPORTS_API_BASE_URL,
                Shield34Properties.DEFAULT_API_BASE_URL)

            Shield34Properties.external_proxy_address = Shield34Properties.get_section_value(
                Shield34PropertiesConstants.PROP_EXTERNAL_PROXY_SECTION,
                Shield34PropertiesConstants.PROP_EXTERNAL_PROXY_ADDRESS,
                None)
            if Shield34Properties.external_proxy_address == '':
                Shield34Properties.external_proxy_address = None

            Shield34Properties.external_proxy_domain = Shield34Properties.get_section_value(
                Shield34PropertiesConstants.PROP_EXTERNAL_PROXY_SECTION,
                Shield34PropertiesConstants.PROP_EXTERNAL_PROXY_DOMAIN,
                None)
            if Shield34Properties.external_proxy_domain == '':
                Shield34Properties.external_proxy_domain = None

            Shield34Properties.external_proxy_username = Shield34Properties.get_section_value(
                Shield34PropertiesConstants.PROP_EXTERNAL_PROXY_SECTION,
                Shield34PropertiesConstants.PROP_EXTERNAL_PROXY_USERNAME,
                None)
            if Shield34Properties.external_proxy_username == '':
                Shield34Properties.external_proxy_username = None

            Shield34Properties.external_proxy_password = Shield34Properties.get_section_value(
                Shield34PropertiesConstants.PROP_EXTERNAL_PROXY_SECTION,
                Shield34PropertiesConstants.PROP_EXTERNAL_PROXY_PASSWORD,
                None)
            if Shield34Properties.external_proxy_password == '':
                Shield34Properties.external_proxy_password = None


            Shield34Properties.enable_ssl_certificate_verification = Shield34Properties.get_section_value(
                Shield34PropertiesConstants.PROP_REPORTS_SECTION,
                Shield34PropertiesConstants.PROP_ENABLE_SSL_CERTIFICATE_VERIFICATION,
                "True")
            Shield34Properties.enable_ssl_certificate_verification = Shield34Properties.enable_ssl_certificate_verification.lower() == 'true'
            Shield34Properties.selenium_proxy_address = Shield34Properties.get_section_value(
                Shield34PropertiesConstants.PROP_PROXY_SECTION,
                Shield34PropertiesConstants.PROP_SELENIUM_PROXY_ADDRESS,
                None)

            if Shield34Properties.selenium_proxy_address == '':
                Shield34Properties.selenium_proxy_address = None

            Shield34Properties.http_library = Shield34Properties.get_section_value(
                Shield34PropertiesConstants.PROP_REPORTS_SECTION,
                Shield34PropertiesConstants.PROP_HTTP_LIBRARY,
                "requests")
            Shield34Properties.isInitialized = True
