from selenium.webdriver.common.by import By

from shield34_reporter.utils.driver_utils import DriverUtils


def shield34_modify_element(by, locator, attribute_name, attribute_value):
    try:
        script = None
        if by is By.ID:
            script = "obj = document.getElementById('" + locator + "');if (obj != null){obj['" + attribute_name + "']='" + attribute_value + "';}"
        if by is By.NAME:
            script = "objects = document.getElementsByName('" + locator + "');if (objects != null ){for(var i=0;i<objects.length;++i){objects[i]['" + attribute_name + "']='" + attribute_value + "';}}"
        if by is By.TAG_NAME:
            script = "objects = document.getElementsByTagName('" + locator + "');if (objects != null ){for(var i=0;i<objects.length;++i){objects[i]['" + attribute_name + "']='" + attribute_value + "';}}"
        if by is By.CLASS_NAME:
            script = "objects = document.getElementsByClassName('" + locator + "');if (objects != null ){for(var i=0;i<objects.length;++i){objects[i]['" + attribute_name + "']='" + attribute_value + "';}}"

        driver = DriverUtils.get_current_driver()
        if driver is not None and script is not None:
            driver.execute_script(script)
    except Exception as e:
        pass


def shield34_remove_element(by, locator):
    try:
        if by is By.ID:
            script = "e = document.getElementById('" + locator + "');if (e != null){};e.remove();";
        if by is By.NAME:
            script = "objects = document.getElementsByName('" + locator + "');if (objects != null ){for(var i=0;i<objects.length;++i){e = objects[i];e.remove();}}"
        if by is By.TAG_NAME:
            script = "objects = document.getElementsByTagName('" + locator + "');if (objects != null ){for(var i=0;i<objects.length;++i){e = objects[i];e.remove();}}"
        if by is By.CLASS_NAME:
            script = "objects = document.getElementsByClassName('" + locator + "');if (objects != null ){for(var i=0;i<objects.length;++i){e = objects[i];e.remove();}}"

        driver = DriverUtils.get_current_driver()
        if driver is not None and script is not None:
            driver.execute_script(script)
    except Exception as e:
        pass