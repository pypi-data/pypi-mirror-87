import click
from typing import Text
from bmlx.utils.import_utils import import_func_from_module
from bmlx.cli.context import pass_bmlx_context
from bmlx.context import BmlxContext


@click.group("job")
def commands():
    pass


@commands.command()
@pass_bmlx_context
@click.option("-T", "--type", type=str, default="")
def list(ctx: BmlxContext, type):
    import_func_from_module("bmlx.cli.handlers.job", "list")(ctx, type)


@commands.command()
@pass_bmlx_context
@click.argument("id", type=int)
def describe(ctx: BmlxContext, id: int):
    import_func_from_module("bmlx.cli.handlers.job", "describe")(ctx, id)
