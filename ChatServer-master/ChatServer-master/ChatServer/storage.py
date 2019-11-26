from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from django.core.files.storage import FileSystemStorage

class MediaS3Storage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION


class StaticS3Storage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION
    
class ConfigS3Storage(S3Boto3Storage):
    location = settings.CONFIGFILES_LOCATION
    default_acl = 'private'    
    file_overwrite = True
    custom_domain = False
    gzip = False
    
    
class ConfigLocalStorage(FileSystemStorage):
    location = settings.CONFIGFILES_LOCATION