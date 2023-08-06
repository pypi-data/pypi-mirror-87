import boto3
from botocore.exceptions import ClientError


class Syncr:
    def __init__(self, service) -> None:
        self._service = service

    def run(self) -> None:
        self._service.run()


class S3:
    def __init__(self):
        self.s3 = boto3.client("s3")
        self._path = None
        self._bucket = None

    @property
    def path(self) -> str:
        return self._path

    @path.setter
    def path(self, path: str) -> None:
        self._path = path

    @property
    def bucket(self) -> str:
        return self._bucket

    @bucket.setter
    def bucket(self, bucket: str) -> None:
        self._bucket = bucket

    def run(self):
        self.s3.upload_file(self.path, self.bucket, self.path)


def sync(syncr: Syncr):
    try:
        syncr.run()
    except ClientError as e:
        raise e
    else:
        return True

