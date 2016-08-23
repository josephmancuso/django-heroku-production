# custom_storages.py
from django.conf import settings
from storages.backends.s3boto import S3BotoStorage


# This code helps store STATIC files (not user uploads) inside Amazon S3
class StaticStorage(S3BotoStorage):
    location = settings.STATICFILES_LOCATION

# This code helps store MEDIA files inside Amazon S3
class MediaStorage(S3BotoStorage):
    location = settings.MEDIAFILES_LOCATION