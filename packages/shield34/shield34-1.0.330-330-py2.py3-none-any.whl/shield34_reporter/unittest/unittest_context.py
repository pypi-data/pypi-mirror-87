import inspect
import unittest
from unittest import TestSuite
from shield34_reporter.listeners.unittest_listener import UnittestListener


class UnittestContext:
    run_name = ''
    current_result_class = None

    @staticmethod
    def attach(result = None, runner = None, run_name='Default suite'):
        UnittestContext.run_name = run_name
        if runner is not None:
            if getattr(runner, 'resultclass', None) is not None:
                UnittestContext.current_result_class = runner.resultclass
                UnittestContext.override_result(runner.resultclass)
            else:
                raise Exception("runner must container resultclass var")

        if result is not None:
            UnittestContext.current_result_class = result
            UnittestContext.override_result(result)
        else:
            UnittestContext.override_suite_run()
            UnittestContext.override_unittest_main()

    @staticmethod
    def override_result(result):
        if getattr(result, '_shield_override', None) is None:
            unittest_listener = UnittestListener(UnittestContext.run_name)
            if not inspect.isclass(result):
                result = type(result)
            if getattr(result, 'startTest', None) is not None:
                UnittestContext.org_start_test = result.startTest

                def shield_test_start(inner_obj, test):
                    unittest_listener.startTest(test)
                    UnittestContext.org_start_test(inner_obj, test)

                result.startTest = shield_test_start

            if getattr(result, 'stopTest', None) is not None:
                UnittestContext.org_stop_test = result.stopTest

                def shield_stop_test(inner_obj, test):
                    unittest_listener.stopTest(test)
                    UnittestContext.org_stop_test(inner_obj, test)

                result.stopTest = shield_stop_test

            if getattr(result, 'startTestRun', None) is not None:
                UnittestContext.org_start_test_run = result.startTestRun

                def shield_start_test_run(inner_obj):
                    unittest_listener.startTestRun()
                    UnittestContext.org_start_test_run(inner_obj)

                result.startTestRun = shield_start_test_run

            if getattr(result, 'stopTestRun', None) is not None:
                UnittestContext.org_stop_test_tun = result.stopTestRun

                def shield_stop_test_run(inner_obj):
                    unittest_listener.stopTestRun()
                    UnittestContext.org_stop_test_tun(inner_obj)

                result.stopTestRun = shield_stop_test_run

            if getattr(result, 'addFailure', None) is not None:
                UnittestContext.org_add_failure = result.addFailure

                def shield_add_failure(inner_obj, test, err):
                    unittest_listener.addFailure(test, err)
                    UnittestContext.org_add_failure(inner_obj, test, err)

                result.addFailure = shield_add_failure

            if getattr(result, 'addSuccess', None) is not None:
                UnittestContext.org_add_success = result.addSuccess

                def shield_add_success(inner_obj, test):
                    unittest_listener.addSuccess(test)
                    UnittestContext.org_add_success(inner_obj, test)

                result.addSuccess = shield_add_success

            if getattr(result, 'addSkip', None) is not None:
                UnittestContext.org_add_skip = result.addSkip

                def shield_add_skip(inner_obj, test, reason):
                    unittest_listener.addSkip(test, reason)
                    UnittestContext.org_add_skip(inner_obj, test, reason)

                result.addSkip = shield_add_skip

            if getattr(result, 'addExpectedFailure', None) is not None:
                UnittestContext.org_add_expected_failure = result.addExpectedFailure

                def shield_add_expected_failure(inner_obj, test, err):
                    unittest_listener.addExpectedFailure(test, err)
                    UnittestContext.org_add_expected_failure(inner_obj, test, err)

                result.addExpectedFailure = shield_add_expected_failure

            if getattr(result, 'addUnexpectedSuccess', None) is not None:
                UnittestContext.org_add_unexpected_success = result.addUnexpectedSuccess

                def shield_add_unexpected_success(inner_obj, test):
                    unittest_listener.addUnexpectedSuccess(test)
                    UnittestContext.org_add_unexpected_success(inner_obj, test)

                result.addUnexpectedSuccess = shield_add_unexpected_success

            if getattr(result, 'addError', None) is not None:
                UnittestContext.org_add_error = result.addError

                def shield_add_error(inner_obj, test, err):
                    unittest_listener.addError(test, err)
                    UnittestContext.org_add_error(inner_obj, test, err)

                result.addError = shield_add_error
            result._shield_override = True

    @staticmethod
    def override_suite_run():
        UnittestContext.org_test_suite_run = TestSuite.run

        def test_suite_run(obj, result, debug=False):
            UnittestContext.current_result_class = result
            UnittestContext.override_result(result)
            UnittestContext.org_test_suite_run(obj,
                                               result, debug)

        TestSuite.run = test_suite_run

    @staticmethod
    def override_unittest_main():
        UnittestContext.org_unittest_main = unittest.main
        def shield_unittest_main( **kwargs):
            if kwargs.get('testRunner', None) is not None:
                testRunner = kwargs.get('testRunner', None)
                if getattr(testRunner, '__init__', None) is not None:
                    UnittestContext.test_runner_org_init = testRunner.__init__

                    def shield_test_runner_init(self, **kwargs):
                        test_runner = UnittestContext.test_runner_org_init(**kwargs)
                        if getattr(test_runner, 'resultclass', None) is not None:
                            UnittestContext.current_result_class = test_runner.resultclass
                            UnittestContext.override_result(test_runner.resultclass)
                        return test_runner

                    testRunner.__init__ = shield_test_runner_init
            else:
                UnittestContext.override_result(unittest.TextTestResult)

            UnittestContext.org_unittest_main(**kwargs)

        unittest.main = shield_unittest_main


