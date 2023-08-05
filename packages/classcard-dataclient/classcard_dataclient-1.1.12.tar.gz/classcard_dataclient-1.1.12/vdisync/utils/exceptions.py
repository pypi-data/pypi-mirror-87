class SyncError(Exception):
    def __init__(self, message=None):
        super(SyncError, self).__init__()
        self.message = message
