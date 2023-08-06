from shield34_reporter.model.csv_rows.report_csv_row import ReportCsvRow
from shield34_reporter.model.enums.row_sub_type import RowSubType
from shield34_reporter.model.enums.row_type import RowType


class LogBaseCsvRow(ReportCsvRow):
    def __init__(self, row_sub_type):
        self.rowType = RowType.LOGS
        super(LogBaseCsvRow, self).__init__(row_sub_type)


class PreDefenseLogCsvRow(LogBaseCsvRow):
    def __init__(self):
        super(PreDefenseLogCsvRow, self).__init__(RowSubType.PRE_DEFENSES)

    def to_array(self):
        return [str(int(round(self.timestamp * 1000.))), str(self.rowSubType.value),str(self.rowType.value), "{}"]