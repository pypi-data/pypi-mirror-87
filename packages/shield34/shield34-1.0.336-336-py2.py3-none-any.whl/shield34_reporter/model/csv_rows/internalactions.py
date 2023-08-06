import json

from shield34_reporter.model.csv_rows.helpers.exception_desc import ExceptionDesc
from shield34_reporter.model.csv_rows.internal_action_csv_row import InternalActionCsvRow
from shield34_reporter.model.enums.row_sub_type import RowSubType


class WaitForElementVisibilityCsvRow(InternalActionCsvRow):
    def __init__(self, timeout, element_is_visible, waiting_time):
        self.timeout = timeout
        self.elementIsVisible = element_is_visible
        self.waitingTime = waiting_time
        super(WaitForElementVisibilityCsvRow, self).__init__(RowSubType.WAIT_FOR_ELEMENT_VISIBILITY)

    def gen_row_value(self, lst=None):
        if lst is None:
            lst = ['timeout', 'elementIsVisible', 'waitingTime']
        row_value = {}
        for a in lst:
            row_value[a] = getattr(self, a)
        return row_value

    def to_array(self):
        return [str(int(round(self.timestamp * 1000.))), str(self.rowSubType.value), str(self.rowType.value), json.dumps(self.gen_row_value())]


class WaitForElementClickabilityCsvRow(InternalActionCsvRow):
    def __init__(self, timeout, element_is_clickable, waiting_time):
        self.timeout = timeout
        self.elementIsClickable = element_is_clickable
        self.waitingTime = waiting_time
        super(WaitForElementClickabilityCsvRow, self).__init__(RowSubType.WAIT_FOR_ELEMENT_CLICKABILITY)

    def gen_row_value(self, lst=None):
        if lst is None:
            lst = ['timeout','elementIsClickable','waitingTime']
        row_value = {}
        for a in lst:
            row_value[a] = getattr(self, a)
        return row_value

    def to_array(self):
        return [str(int(round(self.timestamp * 1000.))), str(self.rowSubType.value), str(self.rowType.value), json.dumps(self.gen_row_value())]


class ElementPositionAtViewPortCsvRow(InternalActionCsvRow):
    def __init__(self, element_position):
        self.elementPosition = element_position
        super(ElementPositionAtViewPortCsvRow, self).__init__(RowSubType.ELEMENT_POSITION_AT_VIEW_PORT)

    def gen_row_value(self, lst=None):
        if lst is None:
            lst = ['elementPosition']
        row_value = {}
        for a in lst:
            row_value[a] = getattr(self, a)
        return row_value

    def to_array(self):
        return [str(int(round(self.timestamp * 1000.))), str(self.rowSubType.value), str(self.rowType.value), json.dumps(self.gen_row_value())]


class PutElementInViewPortCsvRow(InternalActionCsvRow):
    def __init__(self, in_top_of_view_port):
        self.inTopOfViewPort = in_top_of_view_port
        super(PutElementInViewPortCsvRow, self).__init__(RowSubType.PUT_ELEMENT_IN_VIEW_PORT)

    def gen_row_value(self, lst=None):
        if lst is None:
            lst = ['inTopOfViewPort']
        row_value = {}
        for a in lst:
            row_value[a] = getattr(self, a)
        return row_value

    def to_array(self):
        return [str(int(round(self.timestamp * 1000.))), str(self.rowSubType.value), str(self.rowType.value), json.dumps(self.gen_row_value())]


class PerformActionCsvRow(InternalActionCsvRow):
    def __init__(self, action_name, forced):
        self.actionName = action_name
        self.forced = forced
        super(PerformActionCsvRow, self).__init__(RowSubType.PERFORM_ACTION)

    def gen_row_value(self, lst=None):
        if lst is None:
            lst = ['actionName', 'forced']
        row_value = {}
        for a in lst:
            row_value[a] = getattr(self, a)
        return row_value

    def to_array(self):
        return [str(int(round(self.timestamp * 1000.))), str(self.rowSubType.value), str(self.rowType.value), json.dumps(self.gen_row_value())]


class VerifyActionCsvRow(InternalActionCsvRow):
    def __init__(self, verification_passed, action_name):
        self.actionName = action_name
        self.verificationPassed = verification_passed
        super(VerifyActionCsvRow, self).__init__(RowSubType.PERFORM_ACTION)

    def gen_row_value(self, lst=None):
        if lst is None:
            lst = ['actionName', 'verificationPassed']
        row_value = {}
        for a in lst:
            row_value[a] = getattr(self, a)
        return row_value

    def to_array(self):
        return [str(int(round(self.timestamp * 1000.))), str(self.rowSubType.value), str(self.rowType.value), json.dumps(self.gen_row_value())]


class WaitForElementPresenceCsvRow(InternalActionCsvRow):
    def __init__(self, timeout, element_is_present, waiting_time):
        self.timeout = timeout
        self.elementIsPresent = element_is_present
        self.waitingTime = waiting_time
        super(WaitForElementPresenceCsvRow, self).__init__(RowSubType.WAIT_FOR_ELEMENT_PRESENCE)

    def gen_row_value(self, lst=None):
        if lst is None:
            lst = ['timeout', 'elementIsPresent', 'waitingTime']
        row_value = {}
        for a in lst:
            row_value[a] = getattr(self, a)
        return row_value

    def to_array(self):
        return [str(int(round(self.timestamp * 1000.))), str(self.rowSubType.value), str(self.rowType.value), json.dumps(self.gen_row_value())]


class RetryActionCsvRow(InternalActionCsvRow):
    def __init__(self, retry_counter, action_name):
        self.retryCounter = retry_counter
        self.actionName = action_name
        super(RetryActionCsvRow, self).__init__(RowSubType.RETRY_ACTION)

    def gen_row_value(self, lst=None):
        if lst is None:
            lst = ['actionName', 'retryCounter']
        row_value = {}
        for a in lst:
            row_value[a] = getattr(self, a)
        return row_value

    def to_array(self):
        return [str(int(round(self.timestamp * 1000.))), str(self.rowSubType.value), str(self.rowType.value), json.dumps(self.gen_row_value())]


class ExceptionRecoveredCsvRow(InternalActionCsvRow):

    exceptionType = ''
    exception = None
    recovered = True

    def __init__(self, recovered, exception, exception_type):
        self.exception = ExceptionDesc(exception)
        self.exceptionType = exception_type
        self.recovered = recovered
        super(ExceptionRecoveredCsvRow, self).__init__(RowSubType.EXCEPTION_RECOVERED)

    def gen_row_value(self, lst=None):
        if lst is None:
            lst = ['exceptionType', 'exception','recovered']
        row_value = {}
        for a in lst:
            lst_attr = getattr(self, a)
            if hasattr(lst_attr, 'gen_row_value'):
                row_value[a] = lst_attr.gen_row_value()
            else:
                row_value[a] = lst_attr
        return row_value

    def to_array(self):
        return [str(int(round(self.timestamp * 1000.))), str(self.rowSubType.value), str(self.rowType.value), json.dumps(self.gen_row_value())]


class ReallocateElementCsvRow(InternalActionCsvRow):
    locator = ''

    def __init__(self, locator):
        self.locator = locator

        super(ReallocateElementCsvRow, self).__init__(RowSubType.REALLOCATE_ELEMENT)

    def gen_row_value(self, lst=None):
        if lst is None:
            lst = ['locator']
        row_value = {}
        for a in lst:
            row_value[a] = getattr(self, a)
        return row_value

    def to_array(self):
        return [str(int(round(self.timestamp * 1000.))), str(self.rowSubType.value), str(self.rowType.value), json.dumps(self.gen_row_value())]
