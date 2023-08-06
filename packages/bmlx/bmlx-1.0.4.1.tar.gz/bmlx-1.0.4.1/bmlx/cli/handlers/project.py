import os
import pathlib
import sys
import logging
import json
import click

from datetime import datetime
from typing import Text, Optional
from bmlx.utils import io_utils, import_utils, package_utils
from bmlx.flow import Pipeline
from bmlx.context import BmlxContext
from bmlx.cli.constants import BMLX_CONFIG_FILE, BMLX_PIPELINE_ENTRY
from bmlx.cli.cli_exception import BmlxCliException
from bmlx.execution.kubeflow.kubeflow_runner import KubeflowRunner
from bmlx.execution.runner import Runner
from bmlx.execution.multiprocess_runner import MultiProcessRunner
from bmlx import __version__
import bmlx.config as bmlx_config


def info(ctx: BmlxContext, detailed=False):
    click.echo(
        json.dumps(
            {
                "version": __version__,
                "bmlx-components version": package_utils.get_local_package_version(
                    "bmlx-components"
                ),
                "project_name": ctx.project.name,
                "entry": ctx.project.pipeline_path,
                "config_files": [
                    source.filename for source in ctx.project.configs.sources
                ],
            },
            indent=2,
        )
    )


def _upload_local_project(ctx: BmlxContext, pipeline: Pipeline) -> None:
    with ctx.project.packing() as (package, checksum):
        remote_uri = ctx.metadata.upload_package(
            pipeline_storage_path=ctx.pipeline_storage_base,
            experiment=ctx.experiment,
            local_path=package,
            checksum=checksum,
        )
        if not remote_uri:
            logging.warn("uploading package fail")
            return False

        pipeline.meta.uri = remote_uri
        logging.info("upload package success %s (%s)" % (package, checksum))

        # update manifest
        # pipeline.meta.manifest = json.dumps(yaml.safe_load(yaml_content))
        ctx.package, ctx.checksum = package, checksum
        return True


def upload(ctx: BmlxContext, version_alias: Text):
    pipeline = import_utils.import_func_from_source(
        ctx.project.pipeline_path, "create_pipeline"
    )(ctx)

    if not _upload_local_project(ctx=ctx, pipeline=pipeline):
        sys.exit(-1)

    if ctx.engine == "kubeflow":
        runner = KubeflowRunner(ctx=ctx, pipeline=pipeline)
        runner.deploy(version_alias)

    click.echo(
        "Bmlx: upload pipeline %s/%s success, version: %s"
        % (ctx.project.namespace, ctx.project.name, ctx.checksum,)
    )


def run(ctx: BmlxContext, execution_name: Text, execution_description: Text):
    """
    run 是一种轻量级的执行，默认会创建到default experiment，
    """
    pipeline = import_utils.import_func_from_source(
        ctx.project.pipeline_path, "create_pipeline"
    )(ctx)

    # 后面的逻辑会根据 execution_name 获取 pipeline execution context id
    # 本地执行 bmlx run 必须提供 execution_name
    if not execution_name:
        execution_name = f"{pipeline.meta.name}-{datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')}"

    if ctx.local_mode:
        runner = Runner(pipeline=pipeline, ctx=ctx)
        runner.run(
            execution_name=execution_name,
            execution_description=execution_description,
        )
    else:
        if not _upload_local_project(ctx, pipeline):
            sys.exit(-1)
        KubeflowRunner(ctx=ctx, pipeline=pipeline).run(
            execution_name=execution_name,
            execution_description=execution_description,
        )