"""Internal utilities for parsing MLproject YAML files."""

import os
import logging
import pathlib
import glob
import tempfile
import zipfile
import shutil
from distutils.dir_util import copy_tree

from typing import Text, Optional

from bmlx import config as bmlx_config
from bmlx.cli.cli_exception import BmlxCliException
from bmlx.cli.constants import (
    BMLX_CONFIG_FILE,
    BMLX_PIPELINE_ENTRY,
    ARTIFACT_STORAGE_BASE_PATH,
)
from bmlx.utils import io_utils

MY_DIR = os.path.dirname(os.path.realpath(__file__))

_CONFIG_VALIDATION = {
    "name": str,
    "namespace": bmlx_config.String(default=""),
    "description": bmlx_config.String(default=""),
    "local": bmlx_config.Choice([True, False]),
    "entry": bmlx_config.Filename(),
    "package": {"include": bmlx_config.StrSeq(),},
    "parameters": {},
    "pipeline_config": {
        "image": {"name": str, "pull_secrets": str, "pull_policy": str,},
        "components": {"version": str},
    },
}


class _ProjectPackingContext(tempfile.TemporaryDirectory):
    __slots__ = ["_project"]

    def __init__(self, project, runtime_generators=[]):
        self._project = project
        self._project.package = None
        self._project.checksum = None
        self._runtime_generators = runtime_generators
        super(_ProjectPackingContext, self).__init__(prefix=self._project.name)

    def __enter__(self):
        tmpdir = super(_ProjectPackingContext, self).__enter__()
        base_dir = os.path.join(tmpdir, self._project.name)
        for f in self._project._get_package_files():
            rel_path = os.path.relpath(f, self._project.base_path)
            dst_path = os.path.join(base_dir, rel_path)
            if os.path.isdir(f) and not os.path.exists(f):
                shutil.copytree(f, dst_path, copy_function=shutil.copy2)
            else:
                if not os.path.exists(os.path.dirname(dst_path)):
                    os.makedirs(os.path.dirname(dst_path))
                shutil.copy2(f, os.path.join(base_dir, rel_path))

        for generator in self._runtime_generators:
            generator(base_dir)

        # dump the newest configuration into bmlx.yml
        # ctx.project.dump(os.path.join(tmpdir, package_name, BMLX_CONFIG_FILE))
        # archive to zip file
        zip_file = os.path.join(tmpdir, self._project.name + ".zip")
        os.listdir(base_dir)
        cksum = io_utils.zip_dir(base_dir, zip_file)

        self._project.package = zip_file
        self._project.checksum = (
            "r%s" % cksum
        )  # pyyaml could not handle leading zero's with quote, so add a r prefix would fix this issue
        return (self._project.package, self._project.checksum)

    def __exit__(self, exc_type, exc_value, exc_traceback):

        self._project.package = None
        self._project.checksum = None
        super(_ProjectPackingContext, self).__exit__(
            exc_type, exc_value, exc_traceback
        )


class Project(object):
    __slots__ = [
        "_data",
        "name",
        "namespace",
        "description",
        "base_path",
        "artifact_storage_base",
        "bmlx_config_path",
        "pipeline_path",
        "package",
        "checksum",
        "components_version",
    ]

    """A project specification loaded from an BMLX project file in the passed-in directory."""

    def __init__(self, config_name=None, entry=None):
        if config_name is None:
            config_name = BMLX_CONFIG_FILE

        self._locate_config_file(config_name)
        self._load(entry)

    @classmethod
    def load_from_remote(
        cls,
        pipeline_storage_base: Text,
        dst: Text,
        experiment: Text,
        package: Text,
        checksum: Text,
    ):
        with tempfile.TemporaryDirectory() as tmpdir:
            from bmlx.metadata.metadata import Metadata

            ret = Metadata.download_package(
                pipeline_storage_path=pipeline_storage_base,
                experiment=experiment,
                package_name=package,
                checksum=checksum,
                local_dir=tmpdir,
            )
            if not ret:
                raise RuntimeError(
                    "Failed to download package with experiment %s,\
                            package name: %s, checksum: %s"
                    % (experiment, package, checksum)
                )

            with zipfile.ZipFile(
                os.path.join(tmpdir, package + ".zip"), "r"
            ) as zip_ref:
                zip_ref.extractall(tmpdir)
                logging.debug(
                    "extracting package %s/%s to %s"
                    % (experiment, package, tmpdir)
                )
            copy_tree(os.path.join(tmpdir), dst)

    @property
    def configs(self) -> bmlx_config.Configuration:
        return self._data

    @configs.setter
    def configs(self):
        raise AttributeError("data should not set ouside project")

    def packing(self, runtime_generators=[]):
        return _ProjectPackingContext(
            self, runtime_generators=runtime_generators
        )

    def _locate_config_file(self, config_name):
        cur = pathlib.Path(os.getcwd())

        while True:
            conf_file = pathlib.Path(cur, config_name)
            if conf_file.exists():
                self.base_path = cur.as_posix()
                self.bmlx_config_path = conf_file.as_posix()
                break
            if cur.as_posix() == cur.root:
                raise BmlxCliException(
                    "not a bmlx pipeline (or any of the parent directories): bmlx.yml"
                )

            cur = cur.parent

    def _load(self, entry: Optional[Text] = None):
        self._data = bmlx_config.Configuration(
            os.path.join(MY_DIR, "bmlx.yml"), self.bmlx_config_path
        )

        self._data.get(_CONFIG_VALIDATION)  # validate schema

        self.name = self._data["name"].as_str()
        self.namespace = self._data["namespace"].as_str()
        self.description = self._data["description"].as_str()
        self.artifact_storage_base = (
            self._data["pipeline_config"]["artifact_storage_base"].as_str()
            if self._data["pipeline_config"]["artifact_storage_base"].exists()
            else ARTIFACT_STORAGE_BASE_PATH
        )
        self.components_version = self._data["pipeline_config"]["components"][
            "version"
        ].as_str()

        # set base paths
        self._data.relatives = {
            "artifacts": self.artifact_storage_base,
            "project": self.base_path,
        }

        # resolve pipeline entry
        self.pipeline_path = (
            entry or self._data["entry"].as_str() or BMLX_PIPELINE_ENTRY
        )

        logging.debug("detected pipeline base path: %s" % self.pipeline_path)

        if not io_utils.exists(self.pipeline_path):
            raise BmlxCliException(
                "entrypoint not found, please set 'entry' to bmlx.yml or add"
                "a file named 'pipeline.py' in your project"
            )

        logging.debug(
            "loaded project %s, entry_point: %s, base_artifact_storage_path: %s"
            % (self.name, self.pipeline_path, self.artifact_storage_base)
        )

    def resolve_artifact_fs_path(self, path, is_uri=False):
        pure_path = pathlib.PurePath(path)
        if not pure_path.is_absolute():
            pure_path = os.path.join(
                self.artifact_storage_base, pure_path.as_posix()
            )
        else:
            pure_path = pure_path.as_posix()

        return io_utils.resolve_filesystem_and_path(pure_path, is_uri)

    def resolve_project_path(self, path):
        pure_path = pathlib.Path(path)
        if pure_path.is_absolute():
            pure_path = pure_path.as_posix()
        else:
            pure_path = pathlib.Path(self.base_path, path).as_posix()

        return io_utils.resolve_filesystem_and_path(pure_path)

    def _get_package_files(self):
        assert self.base_path
        result = []

        for include in self.configs["package"]["include"].as_str_seq():
            for fn in glob.iglob(
                pathlib.Path(self.base_path, include).as_posix(), recursive=True
            ):
                result.append(fn)

        return result
