"""Utility class for I/O."""
import os
from datetime import datetime
from typing import Text
import zipfile
import yaml
import re
import urllib.parse

from google.protobuf import text_format
from google.protobuf.message import Message
from bmlx.fs.file_system import _stringify_path, LocalFileSystem, S3FileSystem
from bmlx.fs.ceph import CephFileSystem
from bmlx.fs import hdfs

# Nano seconds per second.
NANO_PER_SEC = 1000 * 1000 * 1000

# If path starts with one of those, consider files are in remote filesystem.
_REMOTE_FS_PREFIX = ["hdfs://", "s3://", "http://"]


def get_files_from_timespan(
    base_dir: Text, start_time: datetime, end_time: datetime, time_fmt: Text
):
    data_dir_list = []

    while start_time <= end_time:
        data_dir_list.append(
            "{}/{}".format(base_dir, start_time.strftime(time_fmt))
        )
        start_time += datetime.timedelta(hours=1)
    return data_dir_list


def resolve_filesystem_and_path(where, is_uri=False):
    path = _stringify_path(where)

    parsed_uri = urllib.parse.urlparse(where)

    if parsed_uri.scheme == "hdfs":
        netloc_split = parsed_uri.netloc.split(":")
        host = netloc_split[0]
        if host == "":
            host = "mlcluster"
        else:
            host = parsed_uri.scheme + "://" + host
        port = 0
        if len(netloc_split) == 2 and netloc_split[1].isnumeric():
            port = int(netloc_split[1])
        fs = hdfs.connect(host, port)

        # we keep hdfs path as original hdfs:// format
        if is_uri:
            path = "hdfs://%s%s" % (
                parsed_uri.netloc,
                re.sub(r"/+", r"/", parsed_uri.path),
            )
        else:
            path = re.sub(r"/+", r"/", parsed_uri.path)
    elif parsed_uri.scheme == "s3":
        fs = S3FileSystem.get_instance()
        path = parsed_uri.netloc + "/" + parsed_uri.path
    elif parsed_uri.scheme == "http" and where.find("fs-ceph") > 0:
        fs = CephFileSystem.get_instance()
    else:
        fs = LocalFileSystem.get_instance()
    return fs, path


def mkdirs(uri):
    fs, p = resolve_filesystem_and_path(uri)
    fs.mkdir(uri)


def makedir(uri):
    return mkdirs(uri)


def exists(uri):
    fs, p = resolve_filesystem_and_path(uri)
    return fs.exists(p)


def remove(uri):
    fs, p = resolve_filesystem_and_path(uri)
    return fs.rm(p, recursive=False)


def rmtree(uri):
    fs, p = resolve_filesystem_and_path(uri)
    return fs.rm(p, recursive=True)


def walk(uri):
    fs, p = resolve_filesystem_and_path(uri)
    return fs.walk(p)


def listdir(uri):
    fs, p = resolve_filesystem_and_path(uri)
    return fs.ls(p)


def isdir(uri):
    fs, p = resolve_filesystem_and_path(uri)
    return fs.isdir(p)


def stat(uri):
    fs, p = resolve_filesystem_and_path(uri)
    return fs.stat(p)

def _copyfile(src_fs, src_path, dst_fs, dst_path):
    with dst_fs.open(dst_path, "wb") as o:
        with src_fs.open(src_path, "rb") as i:
            o.write(i.read())

def copy(src, dst):
    src_fs, src_path = resolve_filesystem_and_path(src)
    dst_fs, dst_path = resolve_filesystem_and_path(dst_fs)

    _copyfile(src_fs, src_path, dst_fs, dst_path)

# NOTE: not considred links
def _copytree(src_fs, src_path, dst_fs, dst_path):
    for entry in src_fs.ls(src_path):
        dst_fp = os.path.join(dst_path, os.path.split(entry)[-1])
        if src_fs.isdir(entry):
            if not dst_fs.exists(dst_fp):
                dst_fs.mkdir(dst_fp)
            _copytree(src_fs, entry, dst_fs, dst_fp)
        elif src_fs.isfile(entry):
            _copyfile(src_fs, entry, dst_fs, dst_fp)
        else:
            raise IOError("unsupport file %s" % entry)

def copytree(src, dst):
    src_fs, src_path = resolve_filesystem_and_path(src)
    dst_fs, dst_path = resolve_filesystem_and_path(dst)
    if not dst_fs.exists(dst_path):
        dst_fs.mkdir(dst_path)

    _copytree(src_fs, src_path, dst_fs, dst_path)


def get_only_uri_in_dir(dir_path: Text) -> Text:
    """Gets the only uri from given directory."""
    files = listdir(dir_path)
    if len(files) != 1:
        raise RuntimeError(
            "Only one file per dir is supported: {}.".format(dir_path)
        )
    return files[0]


def delete_dir(path: Text) -> None:
    """Deletes a directory if exists."""

    if isdir(path):
        rmtree(path)


def read_file_string(file_name: Text, binary_mode=False) -> str:
    fs, uri = resolve_filesystem_and_path(file_name)
    with fs.open(uri, "rb") as fd:
        return fd.read()


def write_string_file(file_name: Text, string_value: Text) -> None:
    """Writes a string to file."""
    fs, uri = resolve_filesystem_and_path(file_name)
    with fs.open(uri, "wb") as fd:
        fd.write(string_value)


def write_pbtxt_file(file_name: Text, proto: Message) -> None:
    """Writes a text protobuf to file."""
    write_string_file(file_name, text_format.MessageToString(proto).encode())


def parse_pbtxt_file(file_name: Text, message: Message) -> Message:
    """Parses a protobuf message from a text file and return message itself."""
    contents = read_file_string(file_name)
    text_format.Parse(contents, message)
    return message


def parse_yaml_file(file_name: Text):
    contents = read_file_string(file_name)
    return yaml.load(contents, yaml.Loader)


def all_files_pattern(file_pattern: Text) -> Text:
    """Returns file pattern suitable for Beam to locate multiple files."""
    return "{}*".format(file_pattern)


def generate_fingerprint(split_name: Text, file_pattern: Text) -> Text:
    """Generates a fingerprint for all files that match the pattern."""
    files = []  # glob(file_pattern)
    total_bytes = 0
    # Checksum used here is based on timestamp (mtime).
    # Checksums are xor'ed and sum'ed over the files so that they are order-
    # independent.
    xor_checksum = 0
    sum_checksum = 0
    for f in files:
        s = stat(f)
        total_bytes += s.length
        # Take mtime only up to second-granularity.
        mtime = int(s.mtime_nsec / NANO_PER_SEC)
        xor_checksum ^= mtime
        sum_checksum += mtime

    return (
        "split:%s,num_files:%d,total_bytes:%d,xor_checksum:%d,sum_checksum:%d"
        % (split_name, len(files), total_bytes, xor_checksum, sum_checksum,)
    )


def zip_dir(directory, zipname):
    """
    Compress a directory (ZIP file).
    """
    if os.path.exists(directory):
        with zipfile.ZipFile(zipname, "w", zipfile.ZIP_DEFLATED) as outZipFile:
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    # Write the file named filename to the archive,
                    # giving it the archive name 'arcname'.
                    filepath = os.path.join(dirpath, filename)
                    parentpath = os.path.relpath(filepath, directory)
                    arcname = parentpath

                    outZipFile.write(filepath, arcname)


def download_dir(remote_dir, local_dir):
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    remote_fs, uri = resolve_filesystem_and_path(remote_dir)
    for (root, folders, files) in remote_fs.walk(uri):
        local_root = os.path.join(local_dir, root[len(uri) :].strip("/"))
        for folder_name in folders:
            if not os.path.exists(os.path.join(local_root, folder_name)):
                os.mkdir(os.path.join(local_root, folder_name))
        for f_name in files:
            remote_fs.download(
                os.path.join(root, f_name), os.path.join(local_root, f_name)
            )
            # 文件过大的话，直接 hdfs open 读写会报错，因此用 download 函数
            # with open(os.path.join(local_root, f_name), "wb") as o:
            #     with remote_fs.open(os.path.join(root, f_name), "rb") as i:
            #         o.write(i.read())


def upload_dir(local_dir, remote_dir):
    remote_fs, uri = resolve_filesystem_and_path(remote_dir)
    if not remote_fs.exists(uri):
        remote_fs.mkdir(uri)

    for (root, folders, files) in os.walk(local_dir):
        remote_root = os.path.join(
            remote_dir, root[len(local_dir) :].strip("/")
        )
        for folder_name in folders:
            if not remote_fs.exists(os.path.join(remote_root, folder_name)):
                remote_fs.mkdir(os.path.join(remote_root, folder_name))

        for f_name in files:
            remote_fs.upload(
                os.path.join(root, f_name), os.path.join(remote_root, f_name)
            )
            # 文件过大的话，直接 hdfs open 读写会报错，因此用 upload 函数
            # with remote_fs.open(os.path.join(remote_root, f_name), "wb") as o:
            #     with open(os.path.join(root, f_name), "rb") as i:
            #         o.write(i.read())

if __name__ == "__main__":
    copytree("/data/zhangguanxing/test_copy/src", "s3://mlpipeline/metrics/dst")
