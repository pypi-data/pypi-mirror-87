import time

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

from shield34_reporter.container.run_report_container import RunReportContainer
from shield34_reporter.dynamic_locator.element_dynamic_locator import ElementDynamicLocator
from shield34_reporter.model.csv_rows.debug_exception_log_csv_row import DebugExceptionLogCsvRow
from shield34_reporter.model.csv_rows.helpers import ElementPosition
from shield34_reporter.model.csv_rows.internalactions import WaitForElementVisibilityCsvRow, \
    WaitForElementClickabilityCsvRow, ElementPositionAtViewPortCsvRow, PutElementInViewPortCsvRow, \
    ReallocateElementCsvRow
from shield34_reporter.model.enums.placement import Placement
from shield34_reporter.utils.screen_shots import ScreenShot

current_milli_time = lambda: int(round(time.time() * 1000))

def wait_for_element_visibility_orig(element, web_driver_wait, timeout, action_name):
    if not element.is_displayed():
        try:
            timestamp = current_milli_time()
            wait_for_visibility = WaitForElementVisibility(element)
            web_driver_wait.until(lambda d: wait_for_visibility.is_web_element_visible(d))
            delta = current_milli_time() - timestamp if current_milli_time() - timestamp > 1000 else 0
            RunReportContainer.add_report_csv_row(WaitForElementVisibilityCsvRow(timeout, True, delta))
        except TimeoutException as te:
            RunReportContainer.add_report_csv_row(WaitForElementVisibilityCsvRow(timeout, False, timeout*1000))
            ScreenShot.capture_screen_shoot(action_name.value, Placement.BEFORE.value)
            raise te
        except WebDriverException as wde:
            RunReportContainer.add_report_csv_row(WaitForElementVisibilityCsvRow(timeout, False, 0))
            raise wde


def wait_for_element_visibility(element, web_driver_wait):
    wait_for_visibility = WaitForElementVisibility(element)
    return WebDriverWait.org_until(web_driver_wait, lambda d: wait_for_visibility.is_web_element_visible(d))


def wait_for_element_to_be_enabled(element, web_driver_wait):
    wait_for_enabled = WaitForElementEnabled(element)
    return WebDriverWait.org_until(web_driver_wait, lambda d: wait_for_enabled.is_web_element_enabled(d))


def put_element_in_view_port(driver, element):
    if is_element_totally_in_view_port(driver, element):
        return False
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    return True


def put_element_in_view_port_old(driver, element):
    try:
        if is_element_totally_in_view_port(driver, element):
            RunReportContainer.add_report_csv_row(ElementPositionAtViewPortCsvRow(ElementPosition.AT_VIEW_PORT))
        elif is_element_totally_out_of_view_port(driver,element):
            RunReportContainer.add_report_csv_row(ElementPositionAtViewPortCsvRow(ElementPosition.OUT_OF_VIEW_PORT))
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            RunReportContainer.add_report_csv_row(PutElementInViewPortCsvRow(True))
        else:
            RunReportContainer.add_report_csv_row(ElementPositionAtViewPortCsvRow(ElementPosition.PARTIALLY_AT_VIEW_PORT))
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            RunReportContainer.add_report_csv_row(PutElementInViewPortCsvRow(True))
    except WebDriverException as wde:
        RunReportContainer.add_report_csv_row(DebugExceptionLogCsvRow("putElementInViewPort has Failed", wde))


def is_element_totally_in_view_port(driver, elem):
    elem_left_bound = elem.location.get('x')
    elem_top_bound = elem.location.get('y')
    elem_width = elem.size.get('width')
    elem_height = elem.size.get('height')
    elem_right_bound = elem_left_bound + elem_width
    elem_lower_bound = elem_top_bound + elem_height

    win_upper_bound = driver.execute_script('return window.pageYOffset')
    win_left_bound = driver.execute_script('return window.pageXOffset')
    win_width = driver.execute_script('return document.documentElement.clientWidth')
    win_height = driver.execute_script('return document.documentElement.clientHeight')
    win_right_bound = win_left_bound + win_width
    win_lower_bound = win_upper_bound + win_height

    return all((win_left_bound <= elem_left_bound,
                win_right_bound >= elem_right_bound,
                win_upper_bound <= elem_top_bound,
                win_lower_bound >= elem_lower_bound)
               )


def is_element_totally_out_of_view_port(driver, elem):

    elem_left_bound = elem.location.get('x')
    elem_top_bound = elem.location.get('y')
    elem_width = elem.size.get('width')
    elem_height = elem.size.get('height')
    elem_right_bound = elem_left_bound + elem_width
    elem_lower_bound = elem_top_bound + elem_height

    win_upper_bound = driver.execute_script('return window.pageYOffset')
    win_left_bound = driver.execute_script('return window.pageXOffset')
    win_width = driver.execute_script('return document.documentElement.clientWidth')
    win_height = driver.execute_script('return document.documentElement.clientHeight')
    win_right_bound = win_left_bound + win_width
    win_lower_bound = win_upper_bound + win_height
    return any((elem_right_bound < 0,
                elem_lower_bound < 0,
                elem_left_bound > win_right_bound,
                elem_top_bound > win_lower_bound)
               )


def is_element_totally_out_of_view_port_old(driver, element):
    try:
        window_size = driver.get_window_size()
        window_width = window_size['width']
        window_height = window_size['height']
        element_size = element.size()
        element_location = element.location()
        element_right_x = element_size['width'] + element_location['x']
        element_right_y = element_size['height'] + element_location['y']
        element_left_x = element_location['x']
        element_left_y = element_location['y']
        return element_right_x < 0 or element_right_y < 0 or element_left_x > window_width or element_left_y > window_height
    except Exception as e:
        RunReportContainer.add_report_csv_row(DebugExceptionLogCsvRow("isWebElementTotallyOutOfViewPort has Failed", e))
        return False


def current_milli_time():
    return int(round(time.time() * 1000))


def wait_visibility_pre_defense(element, web_driver_wait, timeout):
    try:
        if not element.is_displayed():
            start = current_milli_time()
            element = wait_for_element_visibility(element, web_driver_wait)
            end = current_milli_time()
            if element is not None:
                RunReportContainer.add_report_csv_row(WaitForElementVisibilityCsvRow(timeout, True, end-start))
    except TimeoutException:
        RunReportContainer.add_report_csv_row(WaitForElementVisibilityCsvRow(timeout, False, timeout))


def wait_enabled_pre_defense(element, web_driver_wait, timeout):
    try:
        if not element.is_displayed():
            start = current_milli_time()
            element = wait_for_element_to_be_enabled(element, web_driver_wait)
            end = current_milli_time()
            if element is not None:
                RunReportContainer.add_report_csv_row(WaitForElementClickabilityCsvRow(timeout, True, end-start) )
    except TimeoutException:
        RunReportContainer.add_report_csv_row(WaitForElementClickabilityCsvRow(timeout, False, timeout))


def wait_for_viewable_pre_defense(driver, element):
    if is_element_totally_in_view_port(driver=driver, elem=element):
        RunReportContainer.add_report_csv_row(ElementPositionAtViewPortCsvRow(ElementPosition.AT_VIEW_PORT));
    else:
        if is_element_totally_out_of_view_port(driver=driver, elem=element):
            RunReportContainer.add_report_csv_row(ElementPositionAtViewPortCsvRow(ElementPosition.OUT_OF_VIEW_PORT))
        else:
            RunReportContainer.add_report_csv_row(ElementPositionAtViewPortCsvRow(ElementPosition.PARTIALLY_AT_VIEW_PORT))
        put_element_in_view_port(driver=driver, element=element)
        RunReportContainer.add_report_csv_row(PutElementInViewPortCsvRow(True))


def click_pre_defenses(driver, element, timeout=10, polling=10):
    try:
        web_driver_wait = WebDriverWait(driver, timeout, polling)
        wait_visibility_pre_defense(element, web_driver_wait, timeout)
        wait_for_viewable_pre_defense(driver, element)
        wait_enabled_pre_defense(element, web_driver_wait, timeout)
    except Exception as e:
        RunReportContainer.add_report_csv_row(DebugExceptionLogCsvRow("Error during click_pre_defenses", e))

def get_element_tag_name(element, driver):
    try:
        if element is None:
            return ""
        return driver.execute_script("return arguments[0].tagName", element)
    except Exception as e:
        RunReportContainer.add_report_csv_row(DebugExceptionLogCsvRow("getElementTagName has Failed", e))
        return ""


def get_element_attribute(element, driver, attr_name):
    try:
        if element is None:
            return ""
        return driver.execute_script("return arguments[0].getAttribute('" + attr_name + "')", element)
    except Exception as e:
        RunReportContainer.add_report_csv_row(DebugExceptionLogCsvRow("getElementTagName has Failed", e))
        return ""



class WaitForElementVisibility(object):
    def __init__(self, element):
        self.web_element = element

    def is_web_element_visible(self, driver):
        if self.web_element.is_displayed():
            return self.web_element

        opacity = driver.execute_script("return window.getComputedStyle(arguments[0], null).getPropertyValue('opacity')",
                                        self.web_element)
        if opacity == "0":
            driver.execute_script("arguments[0].style.opacity=1", self.web_element)
            if self.web_element.is_displayed():
                driver.execute_script("arguments[0].style.opacity=0", self.web_element)
                return self.web_element
            else:
                driver.execute_script("arguments[0].style.opacity=0", self.web_element)
                return None
        return None


class WaitForElementEnabled(WaitForElementVisibility):
    web_element = None

    def __init__(self, element):
        self.web_element = element
        super(WaitForElementEnabled, self).__init__(element)

    def is_web_element_enabled(self, driver):
        if self.web_element.is_enabled():
            return self.web_element
        web_element = self.is_web_element_visible(driver)
        return web_element if web_element is not None and web_element.is_enabled() else None


def reallocate_web_element(driver, web_element):
    element_descriptor = RunReportContainer.get_current_block_run_holder().webElementDescriptorsMap[web_element.id]
    if element_descriptor is not None:
        (relocated_element, current_by, current_value) = ElementDynamicLocator.web_driver_dynamic_find_element(element_descriptor,driver)
        if relocated_element is not None:
            RunReportContainer.add_report_csv_row(ReallocateElementCsvRow(current_by+":"+current_value))
            return relocated_element
    return None
