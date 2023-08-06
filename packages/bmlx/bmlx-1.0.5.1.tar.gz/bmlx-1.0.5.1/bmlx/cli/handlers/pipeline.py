import sys
import click

from typing import Text
from bmlx.execution.runner import Runner
from bmlx.cli.handlers.utils import format_time, list_action
from bmlx.utils.import_utils import import_func_from_source


def list(
    format: Text,
    page_size: int,
    page_token: str,
    local_mode: bool,
    resource_ids=[],
):
    def _f(pipelines):
        return (
            [
                "id",
                "name",
                "ctime",
                "description",
                "default_version_id",
                "default_version_name",
            ],
            [
                (
                    pipeline.id,
                    pipeline.name,
                    format_time(pipeline.create_time),
                    pipeline.description,
                    pipeline.default_version.id,
                    pipeline.default_version.name,
                )
                for pipeline in pipelines
            ],
        )

    list_action(
        resources="pipelines",
        tablulate_func=_f,
        format=format,
        page_size=page_size,
        page_token=page_token,
        local_mode=local_mode,
        resource_ids=resource_ids,
    )


def cleanup(ctx, execution_name, workflow_status):
    """
    clean up pipeline run
    """

    # find pipeline entry
    create_pipeline_func = import_func_from_source(
        ctx.project.pipeline_path, "create_pipeline"
    )
    pipeline = create_pipeline_func(ctx)

    runner = Runner(pipeline, ctx)
    ret = runner.cleanup(
        execution_name=execution_name, workflow_status=workflow_status
    )
    click.echo("pipeline clean up result: %s" % ret)
