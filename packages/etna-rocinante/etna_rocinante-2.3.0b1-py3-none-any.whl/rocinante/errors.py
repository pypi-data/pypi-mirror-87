class RetryableError(Exception):
    """
    Exception wrapper class to mark an error as retryable
    """

    def __init__(self, cause):
        super().__init__()
        self.__cause__ = cause

    def __str__(self):
        return str(self.__cause__)
