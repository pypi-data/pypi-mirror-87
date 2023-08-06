from selenium.webdriver.common.by import By

from shield34_reporter.model.csv_rows.debug_exception_log_csv_row import DebugExceptionLogCsvRow


class WebElementUtils():

    @staticmethod
    def get_elements_html(web_elements):
        if len(web_elements) != 0:
            return WebElementUtils.get_element_html(web_elements[0])

    @staticmethod
    def get_elements_computed_css(web_elements, driver):
        if len(web_elements) != 0:
            return WebElementUtils.get_element_computed_css(web_elements[0], driver)

    @staticmethod
    def get_elements_wrapping_html(web_elements, wrapping_levels):
        if len(web_elements) != 0:
            return WebElementUtils.get_element_wrapping_html(web_elements[0], wrapping_levels)

    @staticmethod
    def get_element_html(web_element):
        from shield34_reporter.container.run_report_container import RunReportContainer
        element_html = ''
        try:
            element_html = web_element.get_attribute("outerHTML")
        except Exception as e:
            RunReportContainer.add_report_csv_row(DebugExceptionLogCsvRow("Couldn't get element html", e))
        return element_html

    @staticmethod
    def get_element_computed_css(web_element, driver):
        from shield34_reporter.container.run_report_container import RunReportContainer

        element_css = ""
        try :
            element_css = driver.execute_script("var cssObj = window.getComputedStyle(arguments[0], null);" +
                                        "var result = {};" +
                                        "for (var i=0; i<cssObj.length; i++) {" +
                                        "cssObjProp = cssObj.item(i);" +
                                        "result[cssObjProp] = cssObj.getPropertyValue(cssObjProp);" +
                                    "}" +
                                    "return JSON.stringify(result);", web_element)
        except Exception as e:
            RunReportContainer.add_report_csv_row(DebugExceptionLogCsvRow("Couldn't calculate element computed css", e))
        return str(element_css)

    @staticmethod
    def get_element_wrapping_html(web_element, wrapping_levels):
        from shield34_reporter.container.run_report_container import RunReportContainer
        i = 0
        element_wrapping_html = ''
        try:
            while i < wrapping_levels and web_element.tag_name != 'body':
                web_element = web_element.org_find_element(By.XPATH, '..')
                i += 1
            element_wrapping_html = web_element.get_attribute("outerHTML")
        except Exception as e:
            RunReportContainer.add_report_csv_row(DebugExceptionLogCsvRow("Couldn't get element wrapping html", e))

        return element_wrapping_html
