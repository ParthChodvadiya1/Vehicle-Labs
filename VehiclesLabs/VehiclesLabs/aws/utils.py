from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

import os
from datetime import datetime
class StaticRootS3BotoStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'
    def get_available_name(self, name, max_length=256):
        now = datetime.now()

        timestamp = datetime.timestamp(now)
        timestamp, d = divmod(timestamp, 1)
        timestamp = int(timestamp)
        ext = name.split('.')[-1]
        filename, ext = os.path.splitext(name)
        name = '%s_%s%s' % (filename, timestamp,ext)
        return name

class MediaRootS3BotoStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False
    def get_available_name(self, name, max_length=256):
        now = datetime.now()

        timestamp = datetime.timestamp(now)
        timestamp, d = divmod(timestamp, 1)
        timestamp = int(timestamp)
        ext = name.split('.')[-1]
        filename, ext = os.path.splitext(name)
        name = '%s_%s%s' % (filename, timestamp,ext)
        return name
