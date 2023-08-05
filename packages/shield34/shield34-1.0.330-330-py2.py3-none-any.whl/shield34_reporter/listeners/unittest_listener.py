import collections
import inspect
import json
import traceback

try:
    from types import SimpleNamespace as Excep
except ImportError:
    from __builtin__ import Exception as Excep

import unittest

from unittest import TestCase

from shield34_reporter.auth.sdk_authentication import SdkAuthentication
from shield34_reporter.exceptions import Shield34PropertiesFileNotFoundException, Shield34PropertiesSyntaxIncorrect, \
    Shield34LoginFailedException
from shield34_reporter.listeners.shield34_listener import Shield34Listener
from shield34_reporter.overrider.selenium_overrider import SeleniumOverrider
from shield34_reporter.utils.logger import Shield34Logger



class UnittestListener():

    shield34_listener = None
    startTestRunCalled = False
    run_name = 'Default Suite'

    def __init__(self, run_name):
        self.run_name = run_name
        self.shield34_listener = Shield34Listener()
        Shield34Logger.init_logging()
        Shield34Logger.override_console_method()
        try:
            Shield34Logger.logger.console("Searching for configuration ini file...")
            SdkAuthentication.login()
            Shield34Logger.logger.console("Logged in successfully to Shield34")
        except Shield34PropertiesFileNotFoundException as e:
            Shield34Logger.logger.warn(e)
        except Shield34PropertiesSyntaxIncorrect as e:
            Shield34Logger.logger.warn(e)
        except Shield34LoginFailedException as e:
            Shield34Logger.logger.warn(e)

    def startTest(self, test=unittest.TestCase):
        if self.startTestRunCalled is False:
            self.startTestRun()
        try:
            test_case_original_attrs = UnittestListener.get_class_attrs(TestCase)
            test_case_attrs = UnittestListener.get_class_attrs(test)
            test_params = UnittestListener.get_test_params(test_case_original_attrs, test_case_attrs)
            test_class_full_name_arr = test.id().split('.')
            test_class_full_name = ''
            if len(test_class_full_name_arr) >= 2:
                test_class_full_name = test_class_full_name_arr[0] + test_class_full_name_arr[1]
            self.shield34_listener.on_test_start(test_name=test._testMethodName, test_class_name=test_class_full_name, block_params=json.dumps(test_params))
        except Shield34PropertiesFileNotFoundException as e:
            Shield34Logger.logger.warn(e)
        except Shield34PropertiesSyntaxIncorrect as e:
            Shield34Logger.logger.warn(e)
        except Shield34LoginFailedException as e:
            Shield34Logger.logger.warn(e)

    def stopTest(self, test=TestCase):
        print("Stopping Test:")

    def startTestRun(self) :
        try:
            self.startTestRunCalled = True
            SeleniumOverrider.override()
            self.shield34_listener.on_suite_start(suite_name=self.run_name)
        except Shield34PropertiesFileNotFoundException as e:
            Shield34Logger.logger.warn(e)
        except Shield34PropertiesSyntaxIncorrect as e:
            Shield34Logger.logger.warn(e)
        except Shield34LoginFailedException as e:
            Shield34Logger.logger.warn(e)

    def stopTestRun(self):
        print("stopping run")

    def addFailure(self, test= TestCase, err = None):
        exception = UnittestListener.build_exception(err, test)
        self.shield34_listener.on_test_failure(exception)
        self.shield34_listener.on_test_finish()

    def addSuccess(self, test= TestCase):
        self.shield34_listener.on_test_success()
        self.shield34_listener.on_test_finish()

    def addSkip(self, test= TestCase, reason=str):
        self.shield34_listener.on_test_skipped()
        self.shield34_listener.on_test_finish()

    def addExpectedFailure(self, test=TestCase,err=None):
        exception = UnittestListener.build_exception(err, test)
        self.shield34_listener.on_test_failure(exception)
        self.shield34_listener.on_test_finish()

    def addUnexpectedSuccess(self, test= TestCase):
        self.shield34_listener.on_test_success()
        self.shield34_listener.on_test_finish()

    def addError(self, test=TestCase, err=None):
        exception = UnittestListener.build_exception(err, test)
        self.shield34_listener.on_test_failure(exception)
        self.shield34_listener.on_test_finish()

    @staticmethod
    def get_class_attrs(class_name):
        class_name_abs = class_name
        if not inspect.isclass(class_name):
            class_name_abs = type(class_name)
        class_attrs = inspect.getmembers(class_name_abs,
                                         lambda a: not (inspect.isroutine(a)) and not (inspect.ismethod(a)) and not (
                                             inspect.isfunction(a)) and not (inspect.isclass(a)) and not (
                                             inspect.isdatadescriptor(a)) and not (inspect.isgetsetdescriptor(a)))
        return class_attrs

    @staticmethod
    def get_test_params(test_case_attrs, called_test_attrs):
        test_params = dict()
        for attr in called_test_attrs:
            called_test_attr_does_not_exists_in_test_case = True
            for test_case_attr in test_case_attrs:
                if test_case_attr[0] == attr[0]:
                    called_test_attr_does_not_exists_in_test_case = False
                    break
            if called_test_attr_does_not_exists_in_test_case:
                param_dict = {attr[0]: attr[1]}
                test_params.update(param_dict)
        sorted_keys = sorted(test_params)
        ordered_test_params = collections.OrderedDict()
        for key in sorted_keys:
            ordered_test_params.update({key: test_params[key]})
        return ordered_test_params

    @staticmethod
    def build_exception(err, test):
        exctype, value, tb = err
        exception = Excep()
        try:
            if 'Assertion' in exctype.__name__:
                exception.assertionError = True
            else:
                exception.assertionError = False

            while tb and UnittestListener._is_relevant_tb_level(tb):
                tb = tb.tb_next

                # Skip assert*() traceback levels
            length = UnittestListener._count_relevant_tb_levels(tb)
            stack_trace_lines = []
            for f_s in traceback.extract_tb(tb, length):
                stack_trace_lines.append(f_s.filename + ' ' + f_s.line)
            exception.stackTrace = stack_trace_lines
            if exctype is test.failureException:
                exception.message = type(value).__name__
            else:
                if getattr(value, 'msg', None) is not None:
                    exception.message = value.msg
        except Exception as e:
            from shield34_reporter.unittest.unittest_context import UnittestContext
            exception_msg = UnittestContext.current_result_class._exc_info_to_string(err, test)
            exception.message = exception_msg

        return exception

    @staticmethod
    def _is_relevant_tb_level(tb):
        return '__unittest' in tb.tb_frame.f_globals

    @staticmethod
    def _count_relevant_tb_levels(tb):
        length = 0
        while tb and not UnittestListener._is_relevant_tb_level(tb):
            length += 1
            tb = tb.tb_next
        return length


