from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions import presence_of_element_located, visibility_of_element_located, \
    element_to_be_clickable
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from shield34_reporter.container.run_report_container import RunReportContainer
from shield34_reporter.dynamic_locator.element_dynamic_locator import ElementDynamicLocator
from shield34_reporter.helpers.web_element_helper import WaitForElementVisibility, WaitForElementEnabled
from shield34_reporter.model.csv_rows.exception_caught_csv_row import ExceptionCaughtCsvRow
from shield34_reporter.model.csv_rows.html.PageHtmlCsvRow import PageHtml
from shield34_reporter.model.csv_rows.html.WebElementHtmlCsvRow import WebElementHtml
from shield34_reporter.model.csv_rows.internalactions import RetryActionCsvRow
from shield34_reporter.model.csv_rows.test_action.action_ended_csv_row import ActionEndedCsvRow
from shield34_reporter.model.csv_rows.test_action.action_started_csv_row import ActionStartedCsvRow
from shield34_reporter.model.csv_rows.web_driver.web_driver_wait_until_csv_row import WebDriverWaitUntilCsvRow
from shield34_reporter.model.enums.exception_type import ExceptionType
from shield34_reporter.model.enums.row_sub_type import RowSubType
from shield34_reporter.utils.driver_utils import DriverUtils
from shield34_reporter.utils.time_utils import TimeUtils
from shield34_reporter.utils.web_element_utils import WebElementUtils


def override():
    WebDriverWait.org_until = WebDriverWait.until

    def shield_until(obj, method, message=''):
        wait_method = wait_method_override(method)
        attributes = ''
        for key in method.__dict__.keys():
            value = str(method.__dict__[key])
            if attributes != '':
                attributes = attributes + ', '
            attributes = attributes + key + '=' + value
        start = TimeUtils.get_current_timestamp()
        try:
            RunReportContainer.add_report_csv_row(ActionStartedCsvRow())
            RunReportContainer.get_current_block_run_holder().in_wait_until = True
            value = WebDriverWait.org_until(obj, wait_method, message)
            end = TimeUtils.get_current_timestamp()

            RunReportContainer.add_report_csv_row(WebDriverWaitUntilCsvRow((end-start)/1000,
                                                                           wait_method.row_sub_type,
                                                                           wait_method.method_name,
                                                                           attributes))
            wait_method.finalize_wait(value)
            return value
        except TimeoutException as te:
            RunReportContainer.get_current_block_run_holder().in_wait_until = False

            RunReportContainer.add_report_csv_row(WebDriverWaitUntilCsvRow(obj._timeout,
                                                                           wait_method.row_sub_type,
                                                                           wait_method.method_name,
                                                                           attributes))

            res = wait_method.timeout_exception(te)
            if res is False:
                raise te
        finally:
            RunReportContainer.add_report_csv_row(ActionEndedCsvRow())

    WebDriverWait.until = shield_until


def wait_method_override(method):
    if isinstance(method, presence_of_element_located):
        return WaitPresenceOfElementLocated(method=method)
    if isinstance(method, visibility_of_element_located):
        return WaitVisibilityOfElementLocated(method)
    if isinstance(method, element_to_be_clickable):
        return WaitElementToBeClickable(method)
    return WaitBase(method)


class WaitBase(object):
    def __init__(self, method):
        self.orig_method = method
        self.row_sub_type = RowSubType.WAIT_FOR_CONDITION
        self.method_name = type(method).__name__

    def __call__(self, driver):
        return self.orig_method(driver)

    def timeout_exception(self, e):
        RunReportContainer.add_report_csv_row(RetryActionCsvRow(1, self.method_name))
        return self(DriverUtils.get_current_driver())

    def finalize_wait(self, wait_result):
        try:
            RunReportContainer.add_report_csv_row(PageHtml(DriverUtils.get_page_html()))
            if wait_result is not None and isinstance(wait_result, WebElement):

                RunReportContainer.get_current_block_run_holder()\
                    .add_web_element(wait_result.id, '')
                RunReportContainer.add_report_csv_row(WebElementHtml(WebElementUtils.get_element_html(wait_result),
                                                                     WebElementUtils.get_element_computed_css(
                                                                         wait_result,
                                                                         DriverUtils.get_current_driver()),
                                                                     WebElementUtils.get_element_wrapping_html(
                                                                         wait_result,
                                                                         3)))

                RunReportContainer.get_current_block_run_holder().add_web_element(wait_result.id, '')
        except Exception as e:
            from shield34_reporter.model.csv_rows.debug_exception_log_csv_row import DebugExceptionLogCsvRow
            RunReportContainer.add_report_csv_row(
                DebugExceptionLogCsvRow("add web element descriptor failed.", e))


class WaitElementToBeClickable(WaitBase):
    def __init__(self, method):
        self.locator = method.locator
        super(WaitElementToBeClickable, self).__init__(method)

    def finalize_wait(self, web_element):
        try:
            RunReportContainer.add_report_csv_row(PageHtml(DriverUtils.get_page_html()))
            if web_element is not None:
                RunReportContainer.get_current_block_run_holder()\
                    .add_web_element(web_element.id, self.locator[0] + ": " + self.locator[1])
                RunReportContainer.add_report_csv_row(WebElementHtml(WebElementUtils.get_element_html(web_element),
                                                                     WebElementUtils.get_element_computed_css(
                                                                         web_element,
                                                                         DriverUtils.get_current_driver()),
                                                                     WebElementUtils.get_element_wrapping_html(
                                                                         web_element,
                                                                         3)))

                RunReportContainer.get_current_block_run_holder().add_web_element(web_element.id,
                                                                                  self.locator[0] + ": " +
                                                                                  self.locator[1])
                web_element_descriptor = ElementDynamicLocator.get_element_descriptor(web_element,
                                                                                      DriverUtils.get_current_driver(),
                                                                                      self.locator[0],
                                                                                      self.locator[1])
                if web_element_descriptor is not None:
                    RunReportContainer.get_current_block_run_holder().webElementDescriptors.append(
                        web_element_descriptor)
        except Exception as e:
            from shield34_reporter.model.csv_rows.debug_exception_log_csv_row import DebugExceptionLogCsvRow
            RunReportContainer.add_report_csv_row(
                DebugExceptionLogCsvRow("add web element descriptor failed.", e))

    def timeout_exception(self, e):

        web_element = ElementDynamicLocator.locate_element_by_element_descriptor(DriverUtils.get_current_driver(),
                                                                                 self.locator[0], self.locator[1])
        if web_element is None:
            raise e
        else:
            wait_for_clickability = WaitForElementEnabled(web_element)
            if wait_for_clickability.is_web_element_enabled(DriverUtils.get_current_driver()):
                self.finalize_wait(web_element)
                return web_element
            else:
                return False


class WaitVisibilityOfElementLocated(WaitBase):
    def __init__(self, method):
        self.locator = method.locator
        super(WaitVisibilityOfElementLocated, self).__init__(method)

    def finalize_wait(self, web_element):
        try:
            RunReportContainer.add_report_csv_row(PageHtml(DriverUtils.get_page_html()))
            if web_element is not None:
                RunReportContainer.get_current_block_run_holder()\
                    .add_web_element(web_element.id, self.locator[0] + ": " + self.locator[1])
                RunReportContainer.add_report_csv_row(WebElementHtml(WebElementUtils.get_element_html(web_element),
                                                                     WebElementUtils.get_element_computed_css(
                                                                         web_element,
                                                                         DriverUtils.get_current_driver()),
                                                                     WebElementUtils.get_element_wrapping_html(
                                                                         web_element,
                                                                         3)))

                RunReportContainer.get_current_block_run_holder().add_web_element(web_element.id,
                                                                                  self.locator[0] + ": " +
                                                                                  self.locator[1])
                web_element_descriptor = ElementDynamicLocator.get_element_descriptor(web_element,
                                                                                      DriverUtils.get_current_driver(),
                                                                                      self.locator[0],
                                                                                      self.locator[1])
                if web_element_descriptor is not None:
                    RunReportContainer.get_current_block_run_holder().webElementDescriptors.append(
                        web_element_descriptor)
        except Exception as e:
            from shield34_reporter.model.csv_rows.debug_exception_log_csv_row import DebugExceptionLogCsvRow
            RunReportContainer.add_report_csv_row(
                DebugExceptionLogCsvRow("add web element descriptor failed.", e))

    def timeout_exception(self, e):
        web_element = ElementDynamicLocator.locate_element_by_element_descriptor(DriverUtils.get_current_driver(),
                                                                                 self.locator[0], self.locator[1])
        if web_element is None:
            raise e
        else:
            wait_for_visibility = WaitForElementVisibility(web_element)
            if wait_for_visibility.is_web_element_visible(DriverUtils.get_current_driver()):
                self.finalize_wait(web_element)
                return web_element
            else:
                return False


class WaitPresenceOfElementLocated(WaitBase):
    def __init__(self, method):
        self.locator = method.locator
        super(WaitPresenceOfElementLocated, self).__init__(method)

    def finalize_wait(self, web_element):
        try:
            RunReportContainer.add_report_csv_row(PageHtml(DriverUtils.get_page_html()))
            if web_element is not None:
                RunReportContainer.get_current_block_run_holder()\
                    .add_web_element(web_element.id, self.locator[0] + ": " + self.locator[1])
                RunReportContainer.add_report_csv_row(WebElementHtml(WebElementUtils.get_element_html(web_element),
                                                                     WebElementUtils.get_element_computed_css(
                                                                         web_element,
                                                                         DriverUtils.get_current_driver()),
                                                                     WebElementUtils.get_element_wrapping_html(
                                                                         web_element,
                                                                         3)))

                RunReportContainer.get_current_block_run_holder().add_web_element(web_element.id,
                                                                                  self.locator[0] + ": " +
                                                                                  self.locator[1])
                web_element_descriptor = ElementDynamicLocator.get_element_descriptor(web_element,
                                                                                      DriverUtils.get_current_driver(),
                                                                                      self.locator[0],
                                                                                      self.locator[1])
                if web_element_descriptor is not None:
                    RunReportContainer.get_current_block_run_holder().webElementDescriptors.append(
                        web_element_descriptor)
        except Exception as e:
            from shield34_reporter.model.csv_rows.debug_exception_log_csv_row import DebugExceptionLogCsvRow
            RunReportContainer.add_report_csv_row(
                DebugExceptionLogCsvRow("add web element descriptor failed.", e))

    def timeout_exception(self, e):
        web_element = ElementDynamicLocator.locate_element_by_element_descriptor(DriverUtils.get_current_driver(),
                                                                                 self.locator[0], self.locator[1])
        if web_element is None:
            raise e
        else:
            self.finalize_wait(web_element)
            return web_element
