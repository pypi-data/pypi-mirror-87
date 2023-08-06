"""
DEFINE required flags of context, this is useful for multi entry project
"""
import click
import functools
import os
import tempfile
from contextlib import ExitStack
from bmlx.utils.var_utils import parse_vars
from bmlx.cli.constants import BMLX_CONFIG_FILE
from bmlx.context import BmlxContext

__context_options = [
    click.option("-n", "--namespace", help="default project namespace"),
    click.option(
        "-f",
        "--file",
        default=BMLX_CONFIG_FILE,
        type=str,
        help="configuration file of this run",
    ),
    click.option(
        "--entry",
        type=str,
        default="",
        help="bmlx entry pipeline file, bmlx will extract from bmlx.yml if 'entry' is not set",
    ),
    click.option(
        "-P",
        "--parameter",
        default=None,
        type=str,
        help="parameter",
        multiple=True,
    ),
    click.option(
        "--dry_run", default=False, is_flag=True, help="just dry run and test"
    ),
    click.option(
        "--local", default=False, is_flag=True, help="remote execution or not"
    ),
    click.option(
        "--engine",
        type=click.Choice(["kubeflow", "local"]),
        default="kubeflow",
        help="if remote mode, ",
    ),
    click.option(
        "--pipeline_storage_base",
        type=str,
        default="hdfs://bigo-rt/user/bmlx/pipeline",
        help="pipeline storage base path",
    ),
    click.option(
        "--experiment", type=str, help="experiment name, default to Default",
    ),
    click.option(
        "--workflow_id", type=str, default="", help="argo workflow id",
    ),
    click.option(
        "--kubeflow_runid", type=str, default="", help="current kubeflow runid",
    ),
]


def pass_bmlx_context(f):
    @click.pass_obj
    def new_func(
        obj,
        pipeline_storage_base,
        engine,
        local,
        namespace,
        experiment,
        file,
        entry,
        parameter,
        dry_run,
        workflow_id,
        kubeflow_runid,
        **kwargs
    ):
        ctx = click.get_current_context()
        bmlx_ctx = ctx.ensure_object(BmlxContext)

        with ExitStack() as stack:
            package = None
            checksum = None
            if (
                kwargs.get("package") is not None
                and kwargs.get("checksum") is not None
            ):
                package = kwargs["package"]
                checksum = kwargs["checksum"]
                tmp = stack.enter_context(
                    tempfile.TemporaryDirectory(prefix=package)
                )
                from bmlx.project_spec import Project

                Project.load_from_remote(
                    pipeline_storage_base=pipeline_storage_base,
                    dst=tmp,
                    experiment=experiment,
                    package=package,
                    checksum=checksum,
                )
                os.chdir(tmp)

            if "package" in kwargs:
                del kwargs["package"]
            if "checksum" in kwargs:
                del kwargs["checksum"]

            bmlx_ctx.init(
                namespace=namespace,
                custom_config_file=file,
                custom_entry_file=entry,
                custom_parameters=parse_vars(parameter),
                dry_run=dry_run,
                local_mode=local,
                engine=engine,
                experiment=experiment,
                workflow_id=workflow_id,
                kubeflow_runid=kubeflow_runid,
            )
            bmlx_ctx.package = package
            bmlx_ctx.checksum = checksum

            f(bmlx_ctx, **kwargs)

    for option in __context_options:
        f = option(f)
    return functools.update_wrapper(new_func, f)
