import json
from shield34_reporter.model.csv_rows.report_csv_row import ReportCsvRow
from shield34_reporter.model.enums.row_type import RowType


class WebDriverWaitUntilCsvRow(ReportCsvRow):
    driver = None

    def __init__(self, timeout, row_sub_type, method_name, attributes):
        self.rowType = RowType.ACTION
        self.timeout = timeout
        self.methodName = method_name
        self.attributes = attributes
        super(WebDriverWaitUntilCsvRow, self).__init__(row_sub_type)

    def gen_row_value(self, lst=None):

        if lst is None:
            lst = ['timeout', 'methodName', 'attributes']
        row_value = {}
        for a in lst:
            lst_attr = getattr(self, a)
            if hasattr(lst_attr, 'gen_row_value'):
                row_value[a] = lst_attr.gen_row_value()
            else:
                row_value[a] = lst_attr
        return row_value

    def to_array(self):
        return [str(int(round(self.timestamp * 1000.))), str(self.rowSubType.value), str(self.rowType.value),
                json.dumps(self.gen_row_value())]
