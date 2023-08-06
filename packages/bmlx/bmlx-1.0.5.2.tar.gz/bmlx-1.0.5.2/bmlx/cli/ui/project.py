import click
from typing import Text
from bmlx.utils.import_utils import import_func_from_module
from bmlx.cli.context import pass_bmlx_context
from bmlx.context import BmlxContext


@click.command()
@pass_bmlx_context
def info(ctx):
    import_func_from_module("bmlx.cli.handlers.project", "info")(ctx)


@click.command()
@click.option(
    "--execution_name", "--en", type=str, default="", help="set execution name"
)
@click.option(
    "--execution_description",
    "--ed",
    type=str,
    default="",
    help="description of exection",
)
@pass_bmlx_context
def run(ctx: BmlxContext, execution_name: Text, execution_description: Text):
    # update plugin
    import_func_from_module("bmlx.cli.handlers.plugin", "update")(
        version=ctx.project.components_version
    )

    # run
    import_func_from_module("bmlx.cli.handlers.project", "run")(
        ctx,
        execution_name=execution_name,
        execution_description=execution_description,
    )


@click.command()
@pass_bmlx_context
@click.option(
    "--version_name", "-v", type=str, default="", help="set execution name"
)
def upload(ctx: BmlxContext, version_name: Text):
    # update plugin
    import_func_from_module("bmlx.cli.handlers.plugin", "update")(
        version=ctx.project.components_version
    )

    import_func_from_module("bmlx.cli.handlers.project", "upload")(
        ctx, version_alias=version_name
    )
