class BaseS3FileDetails(object):
    fileName = ''

    def __init__(self, file_name=''):
        self.fileName = file_name


class BrowserNetworkS3FileDetails(BaseS3FileDetails):

    runId = ''
    blockRunId = ''

    def __init__(self, run_id, block_run_id, file_name = ''):
        self.runId = run_id
        self.blockRunId = block_run_id
        super(BrowserNetworkS3FileDetails, self).__init__(file_name)


class ScreenShotS3FileDetails(BaseS3FileDetails):
    runId = ''
    blockRunId = ''

    def __init__(self, run_id, block_run_id, file_name=''):
        self.runId = run_id
        self.blockRunId = block_run_id
        super(ScreenShotS3FileDetails, self).__init__(file_name)


class TarGzS3FileDetails(BaseS3FileDetails):
    runId = ''
    blockRunId = ''

    def __init__(self, run_id, block_run_id, file_name=''):
        self.runId = run_id
        self.blockRunId = block_run_id
        super(TarGzS3FileDetails, self).__init__(file_name)


class WebElementDescriptorBaseS3FileDetails(BaseS3FileDetails):
    runId = ''
    blockRunId = ''

    def __init__(self, run_id, block_run_id, file_name=''):
        self.runId = run_id
        self.blockRunId = block_run_id
        super(WebElementDescriptorBaseS3FileDetails, self).__init__(file_name)
