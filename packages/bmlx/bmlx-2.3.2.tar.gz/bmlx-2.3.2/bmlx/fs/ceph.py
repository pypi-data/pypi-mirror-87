import boto3
import contextlib
import io
import logging
from bmlx.fs.file_system import FileSystem
from bmlx.config import ConfigError, NotFoundError
from typing import (Text, Dict)
from bmlx.cli.constants import S3_CEPH_STORAGE_MAP

#CEPH_STORAGE_MAP包含可用的所有bucket和对应key
CEPH_STORAGE_MAP = S3_CEPH_STORAGE_MAP
CEPH_ENDPOINT = ""
CEPH_ACCESS_KEY = ""
CEPH_SECRET_KEY = ""
CEPH_BUCKET_NAME = ""


class CephFileSystem(FileSystem):
    _instance = None

    @classmethod
    def get_instance(cls, bucket_name):
        if cls._instance is None:
            return CephFileSystem(bucket_name)

    @classmethod
    #限定对urllib.parse之后的parsed_uri.path使用
    def get_bucket_from_parsed_path(cls, uri:Text):
        if uri == "":
            logging.warning("invalid str to parse")
            return ""
        else:
            uri = uri.lstrip('/')
            return uri.split('/')[0]

    @classmethod
    def get_endpoint_from_bucket(cls, bucket:Text):
        try:
            endpoint = CEPH_STORAGE_MAP[bucket]["endpoint"]
        except NotFoundError:
            raise RuntimeError("Get endpoint from bucket '%s' failed"
            % bucket
        )
        finally:
            return endpoint

    def _resolove_path(self, path):
        # http://fs-ceph-hk.bigo.sg/bmlx-pipeline/{object-name}
        paths = path.split(self.pathsep)
        paths = [p for p in paths if p != ""]
        return paths[2], self.pathsep.join(paths[3:])

    def __init__(self, bucket_name):
        session = boto3.session.Session()
        try:
            if bucket_name == CEPH_BUCKET_NAME:
                self.s3_client = session.client(
                    service_name="s3",
                    endpoint_url=CEPH_ENDPOINT,
                    aws_access_key_id=CEPH_ACCESS_KEY,
                    aws_secret_access_key=CEPH_SECRET_KEY,
                )
            else:
                self.s3_client = session.client(
                    service_name="s3",
                    endpoint_url=CEPH_STORAGE_MAP[bucket_name][
                        "endpoint"],
                    aws_access_key_id=CEPH_STORAGE_MAP[bucket_name][
                        "access_key"],
                    aws_secret_access_key=CEPH_STORAGE_MAP[bucket_name][
                        "secret_key"],
                )
        except NotFoundError:
            raise RuntimeError(
                "CephFileSystem init failed with bucket '%s'." % bucket_name
            )

    @classmethod
    def specify_storage(cls, bucket_name: Text):
        global CEPH_ENDPOINT, CEPH_ACCESS_KEY, CEPH_SECRET_KEY
        try:
            CEPH_BUCKET_NAME = bucket_name
            CEPH_ENDPOINT = CEPH_STORAGE_MAP[bucket_name]["endpoint"]
            CEPH_ACCESS_KEY = CEPH_STORAGE_MAP[bucket_name]["access_key"]
            CEPH_SECRET_KEY = CEPH_STORAGE_MAP[bucket_name]["secret_key"]
        except ConfigError:
            logging.exception("'s3_storage' is not defined, using default value")
            CEPH_BUCKET_NAME = "bmlx-pipeline"
            CEPH_ENDPOINT = "http://fs-ceph-hk.bigo.sg"
            CEPH_ACCESS_KEY = "2TWCN3YQPJ8SOVCWIPAB"
            CEPH_SECRET_KEY = "JwEqpvgeYuFF9OvGR4OOW9A2evKOGFAkdKjr5R7Z"

    @classmethod
    def update_storage_map(cls, new_buckets: Dict[Text, Dict[Text, Text]]):
        global CEPH_STORAGE_MAP
        CEPH_STORAGE_MAP.update(new_buckets)

    def cat(self, path):
        bucket, obj = self._resolove_path(path)
        resp = self.s3_client.get_object(Bucket=bucket, Key=obj)
        return resp["Body"].read()

    def stat(self, path):
        bucket, obj = self._resolove_path(path)
        self.s3_client.head_object(Bucket=bucket, Key=obj)

    def ls(self, path):
        bucket, obj = self._resolove_path(path)
        return [
            o.object_name
            for o in self.s3_client.list_objects(Bucket=bucket, Key=obj)
        ]

    def delete(self, path, recursive=False):
        bucket, obj = self._resolove_path(path)
        self.s3_client.delete_object(Bucket=bucket, Key=obj)

    def disk_usage(self, path):
        raise NotImplementedError()

    def _path_join(self, *args):
        return self.pathsep.join(args)

    def rm(self, path, recursive=False):
        return self.delete(path, recursive=recursive)

    def mv(self, path, new_path):
        return self.rename(path, new_path)

    def rename(self, path, new_path):
        self.copy(path, new_path)
        self.rm(path)

    def copy(self, path, new_path):
        bucket, obj = self._resolove_path(new_path)
        self.s3_client.copy_object(Bucket=bucket, CopySource=obj, Key=path)

    def exists(self, path):
        try:
            self.stat(path)
            return True
        except Exception:
            return False

    def _isfilestore(self):
        return False

    @contextlib.contextmanager
    def open(self, path, mode="rb"):
        bucket, obj = self._resolove_path(path)
        if "w" in mode:
            try:
                b = bytes()
                streaming = io.BytesIO(b)
                yield streaming
            finally:
                streaming.seek(0)
                self.s3_client.put_object(
                    Bucket=bucket,
                    Key=obj,
                    Body=streaming.read(),
                    ContentLength=len(streaming.getbuffer()),
                )
        elif "r" in mode:
            try:
                resp = self.s3_client.get_object(Bucket=bucket, Key=obj)
                yield resp["Body"]
            finally:
                resp["Body"].close()
        else:
            raise RuntimeError("unknown mode %s" % mode)

    @property
    def pathsep(self):
        return "/"
