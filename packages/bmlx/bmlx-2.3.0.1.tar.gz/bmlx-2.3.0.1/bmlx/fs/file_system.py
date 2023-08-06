import os
import io
import abc
import six
import pathlib
import contextlib
import urllib
from os.path import join as pjoin
from minio import Minio
import minio

ENDPOINT = "file-aihk.bigo.sg"
MINIO_ACCESS_KEY = "B7XONTSFOJT6BSU2E54K"
MINIO_SECRET_KEY = "9Rr1g3GChpoYtnrq8oC0ULVurKd7152RafdZtFkj"


class FileSystem:
    """ general file system wrapper """

    @abc.abstractmethod
    def cat(self, path):
        with self.open(path, "rb") as f:
            return f.read()

    @abc.abstractmethod
    def ls(self, path):
        pass

    @abc.abstractmethod
    def delete(self, path, recursive=False):
        pass

    def disk_usage(self, path):
        path = _stringify_path(path)
        path_info = self.stat(path)
        if path_info["kind"] == "file":
            return path_info["size"]

        total = 0
        for root, directories, files in self.walk(path):
            for child_path in files:
                abspath = self._path_join(root, child_path)
                total += self.stat(abspath)["size"]

        return total

    def _path_join(self, *args):
        return self.pathsep.join(args)

    @abc.abstractmethod
    def stat(self, path):
        pass

    def rm(self, path, recursive=False):
        return self.delete(path, recursive=recursive)

    def mv(self, path, new_path):
        return self.rename(path, new_path)

    @abc.abstractmethod
    def rename(self, path, new_path):
        pass

    @abc.abstractmethod
    def mkdir(self, path, create_parents=True):
        pass

    @abc.abstractmethod
    def exists(self, path):
        pass

    @abc.abstractmethod
    def isdir(self, path):
        pass

    @abc.abstractmethod
    def isfile(self, path):
        pass

    @abc.abstractmethod
    def _isfilestore(self):
        pass

    @abc.abstractmethod
    def open(self, path, mode="rb"):
        pass

    @property
    def pathsep(self):
        return "/"


def _stringify_path(path):
    if isinstance(path, six.string_types):
        return path

    try:
        return path.__fspath__()  # new in python 3.6
    except AttributeError:
        if isinstance(path, pathlib.Path):
            return str(path)

    raise TypeError("not a path-like object")


class LocalFileSystem(FileSystem):

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = LocalFileSystem()
        return cls._instance

    def ls(self, path):
        path = _stringify_path(path)
        return sorted(pjoin(path, x) for x in os.listdir(path))

    def mkdir(self, path, create_parents=True):
        path = _stringify_path(path)
        if create_parents:
            os.makedirs(path)
        else:
            os.mkdir(path)

    def isdir(self, path):
        path = _stringify_path(path)
        return os.path.isdir(path)

    def isfile(self, path):
        path = _stringify_path(path)
        return os.path.isfile(path)

    def _isfilestore(self):
        return True

    def exists(self, path):
        path = _stringify_path(path)
        return os.path.exists(path)

    def open(self, path, mode="rb"):
        path = _stringify_path(path)
        return open(path, mode=mode)

    @property
    def pathsep(self):
        return os.path.sep

    def walk(self, path):
        path = _stringify_path(path)
        return os.walk(path)

class S3FileSystem(FileSystem):
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            return S3FileSystem()
    
    def _resolove_path(self, path):
        paths = path.split(self.pathsep)
        paths = [p for p in paths if p!=""]
        return paths[0], self.pathsep.join(paths[1:])

    def __init__(self):
        self.minio = Minio(ENDPOINT, access_key=MINIO_ACCESS_KEY, secret_key=MINIO_SECRET_KEY, secure=True)

    def cat(self, path):
        bucket, obj = self._resolove_path(path)
        data = self.minio.get_object(bucket, obj)
        return data.read()

    def ls(self, path):
        bucket, obj = self._resolove_path(path)
        return [o.object_name for o in self.minio.list_objects(bucket, obj)]

    def delete(self, path, recursive=False):
        bucket, obj = self._resolove_path(path)
        self.minio.remove_object(bucket, obj)

    def disk_usage(self, path):
        raise NotImplementedError()

    def _path_join(self, *args):
        return self.pathsep.join(args)

    def stat(self, path):
        bucket, obj = self._resolove_path(path)
        return self.minio.stat_object(bucket, obj)

    def rm(self, path, recursive=False):
        return self.delete(path, recursive=recursive)

    def mv(self, path, new_path):
        return self.rename(path, new_path)

    def rename(self, path, new_path):
        self.copy(path, new_path)
        self.remove(path)

    def copy(self, path, new_path):
        bucket, obj = self._resolove_path(new_path)
        self.minio.copy_object(bucket, obj, path)

    def mkdir(self, path, create_parents=True):
        paths = path.split(self.pathsep)
        paths = [p for p in paths if p!=""]
        bucket = paths[0]
        cur_path = ""

        for path in paths[1:]:
            cur_path += path + self.pathsep
            try:
                s = self.minio.stat_object(bucket, cur_path)
            except minio.error.NoSuchKey:
                self.minio.put_object(bucket, cur_path, io.BytesIO(), 0)

    def exists(self, path):
        try:
            s = self.stat(path)
            return True
        except minio.error.NoSuchKey:
            return False

    def isdir(self, path):
        try:
            s = self.stat(path)
            return s.is_dir
        except minio.error.NoSuchKey:
            return False

    def isfile(self, path):
        try:
            s = self.stat(path)
            return not s.is_dir
        except minio.error.NoSuchKey:
            return False

    def _isfilestore(self):
        return False

    @contextlib.contextmanager
    def open(self, path, mode="rb"):
        if "w" in mode:
            try:
                bucket, obj = self._resolove_path(path)
                b = bytes()
                streaming = io.BytesIO(b)
                yield streaming
            finally:
                streaming.seek(0)
                self.minio.put_object(bucket, obj, streaming, len(streaming.getbuffer()))
        elif "r" in mode:
            try:
                data = self.minio.get_object(bucket, obj)
                yield data
            finally:
                data.close()
        else:
            raise RuntimeError("unknown mode %s" % mode)
        
        

    @property
    def pathsep(self):
        return "/"

def _is_path_like(path):
    # PEP519 filesystem path protocol is available from python 3.6, so pathlib
    # doesn't implement __fspath__ for earlier versions
    return (
        isinstance(path, six.string_types)
        or hasattr(path, "__fspath__")
        or isinstance(path, pathlib.Path)
    )

