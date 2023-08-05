import json

from shield34_reporter.model.csv_rows.internal_action_csv_row import InternalActionCsvRow
from shield34_reporter.model.enums.row_sub_type import RowSubType


class DynamicElementLocatorCsvRow(InternalActionCsvRow):

    def __init__(self, locator, locator_value):
        self.locator = locator
        self.locator_value = locator_value
        super(DynamicElementLocatorCsvRow, self).__init__(RowSubType.DYNAMIC_ELEMENT_LOCATOR)

    def gen_row_value(self, lst=None):
        if lst is None:
            lst = ['locator','locator_value']
        row_value = {}
        for a in lst:
            row_value[a] = getattr(self, a)
        return row_value

    def to_array(self):
        return [str(int(round(self.timestamp * 1000.))), str(self.rowSubType.value), str(self.rowType.value), json.dumps(self.gen_row_value())]