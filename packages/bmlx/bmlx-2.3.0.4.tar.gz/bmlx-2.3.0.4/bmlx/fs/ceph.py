import boto3
import contextlib
import io
from bmlx.fs.file_system import FileSystem

CEPH_ENDPOINT = "http://fs-ceph-hk.bigo.sg"
CEPH_ACCESS_KEY = "2TWCN3YQPJ8SOVCWIPAB"
CEPH_SECRET_KEY = "JwEqpvgeYuFF9OvGR4OOW9A2evKOGFAkdKjr5R7Z"


class CephFileSystem(FileSystem):
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            return CephFileSystem()

    def _resolove_path(self, path):
        # http://fs-ceph-hk.bigo.sg/bmlx-pipeline/{object-name}
        paths = path.split(self.pathsep)
        paths = [p for p in paths if p != ""]
        return paths[2], self.pathsep.join(paths[3:])

    def __init__(
        self,
        access_key=CEPH_ACCESS_KEY,
        secret_key=CEPH_SECRET_KEY,
        endpoint=CEPH_ENDPOINT,
    ):
        session = boto3.session.Session()
        self.s3_client = session.client(
            service_name="s3",
            aws_access_key_id=CEPH_ACCESS_KEY,
            aws_secret_access_key=CEPH_SECRET_KEY,
            endpoint_url=CEPH_ENDPOINT,
        )

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
