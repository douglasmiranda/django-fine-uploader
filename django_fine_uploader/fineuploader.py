from django.conf import settings as django_settings

from six.moves import range

from os.path import join
from io import StringIO
import shutil

from . import settings
from . import utils


class BaseFineUploader(object):
    def __init__(self, data, *args, **kwargs):
        """About Django file uploads:
        https://docs.djangoproject.com/en/dev/topics/http/file-uploads/

        data: form.cleaned_data
        """
        self.data = data
        self.total_filesize = data.get('qqtotalfilesize')
        self.filename = data.get('qqfilename')
        self.uuid = data.get('qquuid')
        self.file = data.get('qqfile')
        self.storage_class = settings.FILE_STORAGE
        self.real_path = None

    @property
    def finished(self):
        return self.real_path is not None

    @property
    def file_path(self):
        return join(settings.UPLOAD_DIR, self.uuid)

    @property
    def _full_file_path(self):
        return join(self.file_path, self.filename)

    @property
    def storage(self):
        file_storage = utils.import_class(self.storage_class)
        return file_storage()

    def save(self):
        raise NotImplementedError

    def save_on_storage(self, storage_class):
        """So, here is what I'm thinking:
        I want the filesystem storage on ``FU_FILE_STORAGE``.
        But only for as long as the chunks are uploading and combining.
        After that, I want to send them to the real storage, for example,
        AmazonS3.
        """
        raise NotImplementedError

    @property
    def url(self):
        """Final file URL.
        ``self.real_path`` is set when ``self.save()`` is successfull.
        """
        if not self.finished:
            return None
        return self.storage.url(self.real_path)


class SimpleFineUploader(BaseFineUploader):
    def save(self):
        if not self.finished:
            self.real_path = self.storage.save(self._full_file_path, self.file)
        return self.real_path


class ChunkedFineUploader(BaseFineUploader):
    """If you want to know more about chunking with fine uploader:
    http://docs.fineuploader.com/branch/master/features/chunking.html
    And concurrent chunking setting see:
    http://docs.fineuploader.com/branch/master/features/concurrent-chunking.html
    """
    concurrent = True

    def __init__(self, data, concurrent=True, *args, **kwargs):
        super(ChunkedFineUploader, self).__init__(data, *args, **kwargs)
        self.concurrent = concurrent
        self.total_parts = data.get('qqtotalparts')
        self.part_index = data.get('qqpartindex')

    @property
    def chunks_path(self):
        return join(settings.CHUNKS_DIR, self.uuid)

    @property
    def _abs_chunks_path(self):
        return join(django_settings.MEDIA_ROOT, self.chunks_path)

    @property
    def chunk_file(self):
        return join(self.chunks_path, str(self.part_index))

    @property
    def chunked(self):
        return self.total_parts > 1

    @property
    def is_time_to_combine_chunks(self):
        return self.total_parts - 1 == self.part_index

    def combine_chunks(self):
        """Combine a chunked file into a whole file again. Goes through each part,
        in order, and appends that part's bytes to another destination file.

        Discover where the chunks are stored in settings.CHUNKS_DIR
        Discover where the uploads are saved in settings.UPLOAD_DIR
        """
        # So you can see I'm saving a empty file here. That way I'm able to
        # take advantage of django.core.files.storage.Storage.save (and
        # hopefully any other custom Django storage). In a nutshell the
        # ``final_file`` will get a valid name
        # django.core.files.storage.Storage.get_valid_name
        # and I don't need to create some dirs along the way to open / create
        # my ``final_file`` and write my chunks on it.
        # https://docs.djangoproject.com/en/dev/ref/files/storage/#django.core.files.storage.Storage.save
        # In my experience with, for example, custom AmazonS3 storages, they
        # implement the same behaviour.
        self.real_path = self.storage.save(self._full_file_path, StringIO())

        with self.storage.open(self.real_path, 'wb') as final_file:
            for i in range(self.total_parts):
                part = join(self.chunks_path, str(i))
                with self.storage.open(part, 'rb') as source:
                    final_file.write(source.read())
        shutil.rmtree(self._abs_chunks_path)

    def _save_chunk(self):
        return self.storage.save(self.chunk_file, self.file)

    def save(self):
        if self.chunked:
            chunk = self._save_chunk()
            # If ``concurrent=True`` the method self.is_time_to_combine_chunks
            # cannot return an accurate answer, therefore you must call
            # combine_chunks() manually
            if not self.concurrent and self.is_time_to_combine_chunks:
                self.combine_chunks()
                return self.real_path
            return chunk
        else:
            self.real_path = self.storage.save(self._full_file_path, self.file)
            return self.real_path
