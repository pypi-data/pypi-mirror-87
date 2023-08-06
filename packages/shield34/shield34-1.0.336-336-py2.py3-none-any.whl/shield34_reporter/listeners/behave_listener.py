from behave.model_core import Status

from shield34_reporter.auth.sdk_authentication import SdkAuthentication
from shield34_reporter.container.run_report_container import RunReportContainer
from shield34_reporter.listeners.shield34_listener import Shield34Listener
from shield34_reporter.overrider.selenium_overrider import SeleniumOverrider
from shield34_reporter.utils.logger import Shield34Logger
from shield34_reporter.utils.reporter_proxy import ReporterProxy


class Shield34BehaveListener:
    def __init__(self, context):
        try:
            Shield34Logger.init_logging()
            Shield34Logger.override_console_method()
            SdkAuthentication.login()
            self.shield34_listener = Shield34Listener()
            ReporterProxy.start_proxy_management_server()
            self.override = SeleniumOverrider.override()
            RunReportContainer.get_current_run_contract()
            self.behave_context = context
            self.runner = context._runner
            self.hooks = {}
            self.last_exception = None
            self.on_before_all()

        except Exception as e:
            self.shield34_listener = None
            Shield34Logger.logger.console('Did not start Shield34')
            Shield34Logger.logger.warn(e)

    def before_feature(self, feature):
        if self.shield34_listener is not None:
            try:
                #sets the feature name
                RunReportContainer.runContract = None
                self.shield34_listener.on_suite_start(suite_name=feature.name)
            except Exception as e:
                pass

    def after_feature(self, feature):
        if self.shield34_listener is not None:
            RunReportContainer.runContract = None

    def before_scenario(self, scenario):
        if self.shield34_listener is not None:
            try:
                self.last_exception = None
                self.shield34_listener.on_test_start(test_name=scenario.name, test_class_name=scenario.name)
            except Exception as e:
                pass

    def after_scenario(self, scenario):
        if self.shield34_listener is not None:
            try:
                if self.behave_context.failed:
                    if self.last_exception is not None:
                        self.shield34_listener.on_test_failure(self.last_exception)
                elif self.behave_context.aborted:
                    self.shield34_listener.on_test_skipped()
                else:
                    self.shield34_listener.on_test_success()
                self.shield34_listener.on_test_finish()
            except Exception as e:
                pass

    def before_step(self,step):
        pass

    def after_step(self, context, step):
        if step.status == Status.failed:
            self.last_exception = step.exception
        pass

    def on_before_all(self):
        if 'before_feature' in self.runner.hooks:
            self.hooks['before_feature'] = self.runner.hooks['before_feature']
        self.runner.hooks['before_feature'] = self.modified_before_feature

        if 'after_feature' in self.runner.hooks:
            self.hooks['after_feature'] = self.runner.hooks['after_feature']
        self.runner.hooks['after_feature'] = self.modified_after_feature

        if 'before_scenario' in self.runner.hooks:
            self.hooks['before_scenario'] = self.runner.hooks['before_scenario']
        self.runner.hooks['before_scenario'] = self.modified_before_scenario

        if 'after_scenario' in self.runner.hooks:
            self.hooks['after_scenario'] = self.runner.hooks['after_scenario']
        self.runner.hooks['after_scenario'] = self.modified_after_scenario

        if 'before_step' in self.runner.hooks:
            self.hooks['before_step'] = self.runner.hooks['before_step']
        self.runner.hooks['before_step'] = self.modified_before_step

        if 'after_step' in self.runner.hooks:
            self.hooks['after_step'] = self.runner.hooks['after_step']
        self.runner.hooks['after_step'] = self.modified_after_step

    def modified_before_feature(self, context, feature):
        self.before_feature(feature)
        if 'before_feature' in self.hooks:
            self.hooks['before_feature'](context, feature)

    def modified_after_feature(self, context, feature):
        self.after_feature(feature)
        if 'after_feature' in self.hooks:
            self.hooks['after_feature'](context, feature)

    def modified_before_scenario(self, context, scenario):
        self.before_scenario(scenario)
        if 'before_scenario' in self.hooks:
            self.hooks['before_scenario'](context, scenario)

    def modified_after_scenario(self, context, scenario):
        self.after_scenario(scenario)
        if 'after_scenario' in self.hooks:
            self.hooks['after_scenario'](context, scenario)

    def modified_before_step(self, context, step):
        self.before_step(step)
        if 'before_step' in self.hooks:
            self.hooks['before_step'](context, step)

    def modified_after_step(self, context, step):
        self.after_step(context, step)
        if 'after_step' in self.hooks:
            self.hooks['after_step'](context, step)
