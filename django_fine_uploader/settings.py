from django.conf import settings

FILE_STORAGE = getattr(
    settings, 'FU_FILE_STORAGE', 'django.core.files.storage.DefaultStorage'
)

UPLOAD_DIR = getattr(settings, 'FU_UPLOAD_DIR', 'uploads/')

CHUNKS_DIR = getattr(settings, 'FU_CHUNKS_DIR', 'chunks/')

CONCURRENT_UPLOADS = getattr(settings, 'FU_CONCURRENT_UPLOADS', True)

CHUNKS_DONE_PARAM_NAME = getattr(settings, 'FU_CHUNKS_DONE_PARAM_NAME', 'done')
