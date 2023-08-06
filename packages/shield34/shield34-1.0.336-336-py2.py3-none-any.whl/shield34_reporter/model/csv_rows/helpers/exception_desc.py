class ExceptionDesc:

    message = ""
    cause = ""
    assertionError = False
    stackTrace = []
    additionalInfo = ""

    def __init__(self, exception):
        message = ''
        assertion_error = 'false'
        stack_trace = []
        if getattr(exception, 'message', None) is not None:
            message = exception.message
        if getattr(exception, 'msg', None) is not None:
            message = exception.msg
        if getattr(exception, 'longrepr', None) is not None:
            longrepr = getattr(exception, 'longrepr')
            if getattr(longrepr, 'reprcrash', None) is not None:
                message = longrepr.reprcrash.message
        self.message = message

        #self.cause = exception.cause

        if getattr(exception, 'assertionError', None) is not None:
            assertion_error = exception.assertionError
        self.assertionError = assertion_error


        if getattr(exception, 'stackTrace', None) is not None:
            stack_trace = exception.stackTrace
        self.stackTrace = stack_trace

        #self.additionalInfo = exception.additionalInfo

    def gen_row_value(self, lst=['message', 'cause', 'assertionError', 'stackTrace', 'additionalInfo']):
        row_value = {}

        for a in lst:
            row_value[a] = getattr(self, a)
        return row_value
