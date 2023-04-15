import logging
from django.conf import settings


class CloudwatchLoggingFilter(logging.Filter):
    """ Filter which injects context for env on record
    """

    def filter(self, record):
        record.env = settings.ENV
        return True
