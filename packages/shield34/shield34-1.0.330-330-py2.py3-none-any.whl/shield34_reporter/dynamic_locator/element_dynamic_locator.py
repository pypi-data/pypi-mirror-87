import json

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from shield34_reporter import requests
from shield34_reporter.auth.sdk_authentication import SdkAuthentication
from shield34_reporter.consts.js_consts import JsConstants
from shield34_reporter.consts.shield34_properties import Shield34Properties
from shield34_reporter.container.run_report_container import RunReportContainer
from shield34_reporter.model.csv_rows.debug_exception_log_csv_row import DebugExceptionLogCsvRow
from shield34_reporter.model.csv_rows.dynamic_element_locator_csv_row import DynamicElementLocatorCsvRow
from shield34_reporter.model.csv_rows.html.PageHtmlCsvRow import PageHtml
from shield34_reporter.model.csv_rows.test_action.action_ended_csv_row import ActionEndedCsvRow
from shield34_reporter.model.csv_rows.test_action.action_started_csv_row import ActionStartedCsvRow
from shield34_reporter.model.csv_rows.web_driver.web_driver_find_element_csv_row import WebDriverFindElementCsvRow
from shield34_reporter.model.csv_rows.web_driver.web_driver_find_elements_csv_row import WebDriverFindElementsCsvRow
from shield34_reporter.model.csv_rows.web_element.web_element_find_element_csv_row import WebElementFindElementCsvRow
from shield34_reporter.model.csv_rows.web_element.web_element_find_elements_csv_row import WebElementFindElementsCsvRow
from shield34_reporter.model.enums.action_name import ActionName
from shield34_reporter.utils.driver_utils import DriverUtils
from shield34_reporter.utils.external_proxy import get_external_proxies
from shield34_reporter.utils.import_utils import is_module_available


class ElementDynamicLocator():

    descriptors_to_locate_by = ['xpath_with_id', 'xpath_with_index']
    attributes_to_locate_by= ['id', 'class']

    @staticmethod
    def get_element_descriptor(web_element, driver, by, value):
        element_descriptor = dict()
        try:
            element_xpath_with_index = ElementDynamicLocator.get_element_xpath_with_index(web_element, driver)
            element_xpath_with_id = ElementDynamicLocator.get_element_xpath_with_id(web_element, driver)
            element_attributes = ElementDynamicLocator.get_element_attributes(web_element, driver)
            element_locator = by + ": " + value
            element_descriptor = dict(locator=element_locator, xpath_with_index=element_xpath_with_index,
                                      xpath_with_id=element_xpath_with_id)
            element_descriptor['attributes'] = dict()
            for attribute in element_attributes:
                element_descriptor['attributes'][attribute['nodeName']] = attribute['nodeValue']
        except Exception as e:
            RunReportContainer.add_report_csv_row(
                DebugExceptionLogCsvRow("create web element descriptor failed.", e))

        return element_descriptor

    @staticmethod
    def get_element_attributes(web_element, driver):
        all_attributes = []
        if web_element is None or driver is None:
            return []
        try:
            all_attributes = driver.execute_script("return arguments[0].attributes", web_element)
        except Exception as e:
            RunReportContainer.add_report_csv_row(DebugExceptionLogCsvRow("ElementDynamicLocator getElementAttributes failed", e))

        return all_attributes

    @staticmethod
    def get_element_xpath_with_index(web_element, driver):
        element_xpath = ''
        if web_element is None or driver is None:
            return element_xpath
        try:
            element_xpath = driver.execute_script(JsConstants.get_element_xpath_with_index_script, web_element)
        except Exception as e:
            RunReportContainer.add_report_csv_row(DebugExceptionLogCsvRow("ElementDynamicLocator getElementXpath with index failed.", e))

        return element_xpath

    @staticmethod
    def get_element_xpath_with_id(web_element, driver):
        element_xpath = ''
        if web_element is None or driver is None:
            return element_xpath
        try:
            element_xpath = driver.execute_script(JsConstants.get_element_xpath_with_id_script, web_element)
        except Exception as e:
            RunReportContainer.add_report_csv_row(
                DebugExceptionLogCsvRow("ElementDynamicLocator getElementXpath with id failed.", e))

        return element_xpath


    @staticmethod
    def get_dynamic_elements_locating_descriptors():
        if SdkAuthentication.isAuthorized:
            headers = {'content-type': 'application/json',
                       'Authorization': 'Shield34-Project ' + SdkAuthentication.get_user_token()}
            block_contract = RunReportContainer.get_current_block_run_holder().blockRunContract.blockContract
            request = requests.get(Shield34Properties.api_base_url + '/dynamic-element-locator/get',
                                   params={'blockId': block_contract.id},
                                   headers=headers, verify=Shield34Properties.enable_ssl_certificate_verification,
                                   proxies=get_external_proxies())
            if request.status_code == 200:
                response_data = request.json()['data']
                if response_data == '':
                    RunReportContainer.get_current_block_run_holder().dynamicElementsLocatorForBlockExistsInS3 = False
                else:
                    RunReportContainer.get_current_block_run_holder().dynamicElementsLocator = json.loads(request.json()['data'])
                    RunReportContainer.get_current_block_run_holder().dynamicElementsLocatorForBlockExistsInS3 = True
            else:
                RunReportContainer.get_current_block_run_holder().dynamicElementsLocatorForBlockExistsInS3 = False

    @staticmethod
    def is_dynamic_element_locating_descriptor_exists():
        if len(
                RunReportContainer.get_current_block_run_holder().dynamicElementsLocator) == 0 and RunReportContainer.get_current_block_run_holder().dynamicElementsLocatorForBlockExistsInS3 is None:
            ElementDynamicLocator.get_dynamic_elements_locating_descriptors()

        if RunReportContainer.get_current_block_run_holder().dynamicElementsLocatorForBlockExistsInS3 is True and len(
                RunReportContainer.get_current_block_run_holder().dynamicElementsLocator) != 0:
            return True
        else:
            return False




    @staticmethod
    def get_current_find_element_dynamic_locator_descriptor():
        if ElementDynamicLocator.is_dynamic_element_locating_descriptor_exists():
            current_find_element_index = RunReportContainer.get_current_block_run_holder().findElementCounter
            if current_find_element_index < len(RunReportContainer.get_current_block_run_holder().dynamicElementsLocator):
                return RunReportContainer.get_current_block_run_holder().dynamicElementsLocator[current_find_element_index]
            else:
                return None
        else:
            return None

    @staticmethod
    def locate_elements_by_element_descriptor(driver_or_element, by, value):
        current_element_descriptor = ElementDynamicLocator.get_current_find_element_dynamic_locator_descriptor()
        element_locator = by + ": " + value
        web_elements = None
        if current_element_descriptor is not None:
            if element_locator == current_element_descriptor['locator']:
                #web driver find element case
                if isinstance(driver_or_element, WebDriver):
                    web_elements = ElementDynamicLocator.web_driver_dynamic_find_elements(current_element_descriptor, driver_or_element)
                #web element find element case
                else:
                    web_elements = ElementDynamicLocator.web_element_dynamic_find_elements(current_element_descriptor, driver_or_element)

                if web_elements[0] is not None:
                    if len(web_elements[0]) > 0 and len(web_elements) == 3:
                        ElementDynamicLocator.dynamic_element_add_to_console_log(by, value, web_elements[1], web_elements[2])
        if web_elements is not None:
            return web_elements[0]
        return web_elements

    @staticmethod
    def locate_element_by_element_descriptor(driver_or_element, by, value):
        current_element_descriptor = ElementDynamicLocator.get_current_find_element_dynamic_locator_descriptor()
        web_element = None
        element_locator = by + ": " + value
        if current_element_descriptor is not None:
            if element_locator == current_element_descriptor['locator']:
                #web driver find element case
                if isinstance(driver_or_element, WebDriver):
                    web_element = ElementDynamicLocator.web_driver_dynamic_find_element(current_element_descriptor, driver_or_element)
                #web element find element case
                else:
                    web_element = ElementDynamicLocator.web_element_dynamic_find_element(current_element_descriptor, driver_or_element)

                if web_element[0] is not None and len(web_element) == 3:
                    ElementDynamicLocator.dynamic_element_add_to_console_log(by, value, web_element[1], web_element[2])
        if web_element is not None:
            return web_element[0]
        return web_element

    @staticmethod
    def internal_web_driver_find_element(driver, by, value):
        from shield34_reporter.overrider.selenium_overrider import SeleniumOverrider
        web_element = None

        try:
            RunReportContainer.add_report_csv_row(DynamicElementLocatorCsvRow(by, value))
            web_element = WebDriver.org_find_element(driver, by, value)
            RunReportContainer.get_current_block_run_holder().add_web_element(web_element.id, by + ": " + value)
        except Exception as e:
            raise e
        return web_element

    @staticmethod
    def internal_web_driver_find_elements(driver, by, value):
        from shield34_reporter.overrider.selenium_overrider import SeleniumOverrider
        RunReportContainer.add_report_csv_row(DynamicElementLocatorCsvRow(by, value))
        try:
            located_web_elements = WebDriver.org_find_elements(driver, by, value)
            for elem in located_web_elements:
                RunReportContainer.get_current_block_run_holder().add_web_element(elem.id, by + ": " + value)
        except Exception as e:
            raise e
        return located_web_elements

    @staticmethod
    def internal_web_element_find_element(parent_web_element, by, value):
        from shield34_reporter.overrider.selenium_overrider import SeleniumOverrider
        web_element = None
        RunReportContainer.add_report_csv_row(DynamicElementLocatorCsvRow(by, value))
        try:
            web_element = WebElement.org_find_element(parent_web_element, by, value)
            RunReportContainer.get_current_block_run_holder().add_web_element(web_element.id, by + ": " + value)
        except Exception as e:
            raise e
        return web_element

    @staticmethod
    def internal_web_element_find_elements(parent_web_element, by, value):
        from shield34_reporter.overrider.selenium_overrider import SeleniumOverrider
        try:
            RunReportContainer.add_report_csv_row(DynamicElementLocatorCsvRow(by, value))
            located_web_elements = WebElement.org_find_elements(parent_web_element, by, value)
            for elem in located_web_elements:
                RunReportContainer.get_current_block_run_holder().add_web_element(elem.id, by + ": " + value)
        except Exception as e:
            raise e
        return located_web_elements


    @staticmethod
    def web_driver_dynamic_find_element(current_element_descriptor, driver):
        web_element = None
        current_by = None
        current_value = None
        try:
            current_by = 'xpath'
            current_value = current_element_descriptor['xpath_with_id']
            web_element = ElementDynamicLocator.internal_web_driver_find_element(driver, By.XPATH, current_element_descriptor['xpath_with_id'])
        except Exception as e:
            RunReportContainer.add_report_csv_row(
                DebugExceptionLogCsvRow("Couldn't re-allocate element by xpath with id", e))
        if web_element is None:
            try:
                current_by = 'xpath'
                current_value = current_element_descriptor['xpath_with_index']
                web_element = ElementDynamicLocator.internal_web_driver_find_element(driver, By.XPATH, current_element_descriptor['xpath_with_index'])
            except Exception as e:
                RunReportContainer.add_report_csv_row(
                    DebugExceptionLogCsvRow("Couldn't re-allocate element by xpath with index", e))
        if web_element is None:

            if 'id' in current_element_descriptor['attributes']:
                try:
                    current_by = 'id'
                    current_value = current_element_descriptor['attributes']['id']
                    web_element = ElementDynamicLocator.internal_web_driver_find_element(driver, By.ID, current_element_descriptor['attributes']['id'])
                except Exception as e:
                    RunReportContainer.add_report_csv_row(
                        DebugExceptionLogCsvRow("Couldn't re-allocate element by xpath with index", e))
        return web_element, current_by, current_value

    @staticmethod
    def web_driver_dynamic_find_elements(current_element_descriptor, driver):
        web_elements = None
        current_by = None
        current_value = None
        try:
            current_by = 'xpath'
            current_value = current_element_descriptor['xpath_with_id']
            web_elements = ElementDynamicLocator.internal_web_driver_find_elements(driver, By.XPATH, current_element_descriptor['xpath_with_id'])
        except Exception as e:
            RunReportContainer.add_report_csv_row(
                DebugExceptionLogCsvRow("Couldn't re-allocate element by xpath with id", e))
        if web_elements is None or len(web_elements) == 0:
            try:
                current_by = 'xpath'
                current_value = current_element_descriptor['xpath_with_index']
                web_elements = ElementDynamicLocator.internal_web_driver_find_elements(driver, By.XPATH, current_element_descriptor['xpath_with_index'])
            except Exception as e:
                RunReportContainer.add_report_csv_row(
                    DebugExceptionLogCsvRow("Couldn't re-allocate element by xpath with index", e))
        if web_elements is None or len(web_elements) == 0:

            if 'id' in current_element_descriptor['attributes']:
                try:
                    current_by = 'id'
                    current_value = current_element_descriptor['attributes']['id']
                    web_elements = ElementDynamicLocator.internal_web_driver_find_elements(driver, By.ID,
                                                                                           current_element_descriptor['attributes']['id'])
                except Exception as e:
                    RunReportContainer.add_report_csv_row(
                        DebugExceptionLogCsvRow("Couldn't re-allocate element by xpath with index", e))
        return web_elements, current_by, current_value

    @staticmethod
    def web_element_dynamic_find_element(current_element_descriptor, parent_web_element):
        web_element = None
        current_by = None
        current_value = None
        try:
            current_by = 'xpath'
            current_value = current_element_descriptor['xpath_with_id']
            web_element = ElementDynamicLocator.internal_web_element_find_element(
                parent_web_element,
                By.XPATH,
                current_element_descriptor['xpath_with_id'])
        except Exception as e:
            RunReportContainer.add_report_csv_row(
                DebugExceptionLogCsvRow("Couldn't re-allocate element by xpath with id", e))
        if web_element is None:
            try:
                current_by = 'xpath'
                current_value = current_element_descriptor['xpath_with_index']
                web_element = ElementDynamicLocator.internal_web_element_find_element(parent_web_element,
                                                                                      By.XPATH,
                                                                                      current_element_descriptor['xpath_with_index'])
            except Exception as e:
                RunReportContainer.add_report_csv_row(
                    DebugExceptionLogCsvRow("Couldn't re-allocate element by xpath with index", e))
        if web_element is None:

            if 'id' in current_element_descriptor['attributes']:
                try:
                    current_by = 'id'
                    current_value = current_element_descriptor['attributes']['id']
                    web_element = ElementDynamicLocator.internal_web_element_find_element(
                        parent_web_element,
                        By.ID,
                        current_element_descriptor['attributes']['id'])
                except Exception as e:
                    RunReportContainer.add_report_csv_row(
                        DebugExceptionLogCsvRow("Couldn't re-allocate element by xpath with index", e))
        return web_element, current_by, current_value

    @staticmethod
    def web_element_dynamic_find_elements(current_element_descriptor, parent_web_element):
        web_elements = None
        current_by = None
        current_value = None
        try:
            current_by = 'xpath'
            current_value = current_element_descriptor['xpath_with_id']
            web_elements = ElementDynamicLocator.internal_web_element_find_elements(
                parent_web_element,
                By.XPATH,
                current_element_descriptor['xpath_with_id'])
        except Exception as e:
            RunReportContainer.add_report_csv_row(
                DebugExceptionLogCsvRow("Couldn't re-allocate element by xpath with id", e))
        if web_elements is None or len(web_elements) == 0:
            try:
                current_by = 'xpath'
                current_value = current_element_descriptor['xpath_with_index']
                web_elements = ElementDynamicLocator.internal_web_element_find_elements(
                    parent_web_element,
                    By.XPATH,
                    current_element_descriptor['xpath_with_index'])
            except Exception as e:
                RunReportContainer.add_report_csv_row(
                    DebugExceptionLogCsvRow("Couldn't re-allocate element by xpath with index", e))
        if web_elements is None or len(web_elements) == 0:

            if 'id' in current_element_descriptor['attributes']:
                try:
                    current_by = 'id'
                    current_value = current_element_descriptor['attributes']['id']
                    web_elements = ElementDynamicLocator.internal_web_element_find_elements(
                        parent_web_element,
                        By.ID,
                        current_element_descriptor['attributes']['id'])
                except Exception as e:
                    RunReportContainer.add_report_csv_row(
                        DebugExceptionLogCsvRow("Couldn't re-allocate element by xpath with index", e))
        return web_elements, current_by, current_value


    @staticmethod
    def dynamic_element_add_to_console_log(by, value, dynamic_by, dynamic_value):
        if is_module_available('robot'):
            from robot.libraries.BuiltIn import BuiltIn
