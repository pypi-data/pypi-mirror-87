# encoding: utf-8
import six
import boto3
import posixpath
from django.conf import settings
from botocore.exceptions import ClientError


class S3(object):
    """S3客户端封装"""

    def __init__(
        self,
        host=settings.S3['host'],
        port=settings.S3['port'],
        access_key=settings.S3['access_key'],
        secret_key=settings.S3['secret_key'],
        bucket=settings.S3['bucket'],
        key=None,
    ):
        """TODO: to be defined1.

        :host: TODO
        :port: TODO
        :access_key: TODO
        :secret_key: TODO
        :bucket: TODO
        :key: TODO

        """
        self._bucket = bucket
        self._key = key
        _port = port and int(port) not in (80, 443) and f":{port}" or ""
        protocol = port and int(port) == 443 and "https" or "http"
        self._host = "{}://{}{}".format(protocol, host, _port)

        session = boto3.session.Session()
        self._client = session.client(
            service_name="s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url=self._host,
        )

    @property
    def url(self):
        return self._host + "/" + self._bucket + "/" + self._key

    def download(self, key, path=None):
        """下载S3文件

        :key: S3上的路径
        :path: 下载到的本地路径，如果为空，则返回bytesio
        :returns: file like obj

        """
        if path:
            return self._client.download_file(self._bucket, key, path)
        bio = six.BytesIO()
        self._client.download_fileobj(self._bucket, key, bio)
        bio.seek(0)
        return bio

    def upload(self, path, key, perm=None):
        """上传S3文件

        :path: 上传的文件 本地路径或者bytesio
        :key: S3上的路径
        :perm: 权限 public| private
        :returns: file like obj

        """
        if isinstance(path, str):
            return self._client.upload_file(path, self._bucket, key)
        return self._client.upload_fileobj(path, self._bucket, key)

    def putACL(self, key, ACL):
        """设置文件权限

        :key: S3上文件路径
        :ACL: private|public-read
        """
        self._client.put_object_acl(ACL=ACL, Bucket=self._bucket, Key=key)

    def listdir(self, path):
        if path and not path.endswith('/'):
            path += '/'
        directories = []
        files = []
        paginator = self._client.get_paginator('list_objects')
        pages = paginator.paginate(Bucket=self._bucket, Delimiter='/', Prefix=path)
        for page in pages:
            for entry in page.get('CommonPrefixes', ()):
                directories.append(posixpath.relpath(entry['Prefix'], path))
            for entry in page.get('Contents', ()):
                files.append(posixpath.relpath(entry['Key'], path))
        return directories, files

    def exists(self, name):
        try:
            self._client.head_object(Bucket=self._bucket, Key=name)
            return True
        except ClientError:
            return False

    def delete(self, name):
        self._client.delete_object(Bucket=self._bucket, Key=name)

    def move(self, key, name):
        copy_source = {'Bucket': self._bucket, 'Key': key}
        self._client.copy_object(CopySource=copy_source, Bucket=self._bucket, Key=name)
        self._client.delete_object(**copy_source)

    def copy(self, key, name):
        copy_source = {'Bucket': self._bucket, 'Key': key}
        self._client.copy_object(CopySource=copy_source, Bucket=self._bucket, Key=name)

    def close_connection(self):
        pass
