import os

from tempfile import gettempdir
from shutil import copyfile

from spintop.models import BaseDataClass

from google.cloud import storage

class FileReference(BaseDataClass):
    name: str

    def download_to_filename(self, filename):
        copyfile(self.name, filename)
    
    def download_temp(self):
        filename = os.path.join(gettempdir(), self.bucket, self.name)

        folder, _ = os.path.split(filename)
        os.makedirs(folder, exist_ok=True)

        self.download_to_filename(filename)
        return filename

class GCSFileReference(FileReference):
    bucket: str

    def download_to_filename(self, filename):
        storage_client = storage.Client()

        bucket = storage_client.bucket(self.bucket)
        blob = bucket.blob(self.name)
        blob.download_to_filename(filename)
    
    def download_temp(self):
        filename = os.path.join(gettempdir(), self.bucket, self.name)

        folder, _ = os.path.split(filename)
        os.makedirs(folder, exist_ok=True)

        self.download_to_filename(filename)
        return filename

def list_bucket_files(bucket_name):
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucket_name)
    return [GCSFileReference(bucket=bucket_name, name=blob.name) for blob in blobs]