import pytest

from shield34_reporter.auth.sdk_authentication import SdkAuthentication
from shield34_reporter.exceptions import Shield34PropertiesFileNotFoundException, Shield34PropertiesSyntaxIncorrect, \
    Shield34LoginFailedException
from shield34_reporter.listeners.shield34_listener import Shield34Listener
from shield34_reporter.model.enums.status import Status
from shield34_reporter.overrider.selenium_overrider import SeleniumOverrider
from shield34_reporter.utils.logger import Shield34Logger


def pytest_addoption(parser):
    group = parser.getgroup('shield34_reporter', 'Shield34 Reporter')
    group.addoption('--shield34-reporter')

def pytest_configure(config):
    if not config.option.shield34_reporter:
        return
    config._shield34reporter = Shield34Reporter(config)
    config.pluginmanager.register(config._shield34reporter)

class Shield34Reporter:

    shield34_listener = Shield34Listener()

    def __init__(self, config):
        self.config = config
        Shield34Logger.override_console_method()
        SdkAuthentication.login()
        SeleniumOverrider.override()


    #this is on suite start!
    def pytest_sessionstart(self, session):
        self.shield34_listener.on_suite_start(suite_name=session.name)


    # this hood is for on test start
    @pytest.hookimpl(tryfirst=True)
    def pytest_runtest_logstart(self, nodeid, location):
        self.shield34_listener.on_test_start(test_name=location[2], test_class_name=location[0])

    # on test finish !

    def pytest_runtest_logreport(self, report):
        if report.when == 'call':
            if report.passed:
                self.shield34_listener.on_test_success()
                self.shield34_listener.on_test_finish()

            elif report.failed:
                self.shield34_listener.on_test_failure(report)
                self.shield34_listener.on_test_finish()

            elif report.skipped:
                self.shield34_listener.on_test_skipped()
                self.shield34_listener.on_test_finish()

            from shield34_reporter.container.run_report_container import RunReportContainer
            block_run_contract = RunReportContainer.get_current_block_run_holder().prevBlockRunContract
            if block_run_contract is not None:
                from shield34_reporter.listeners.listener_utils import ListenerUtils
                shield34_url = ListenerUtils.get_test_run_url(block_run_contract)
                Shield34Logger.logger.console("\nShield34 Report Url: " + shield34_url)









