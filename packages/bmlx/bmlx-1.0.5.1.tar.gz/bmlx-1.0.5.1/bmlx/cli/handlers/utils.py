import datetime
import click
import json
import yaml

from typing import Text
from tabulate import tabulate
from google.protobuf import json_format
from bmlx.metadata.metadata import Metadata


def format_time(ts: int):
    return datetime.datetime.fromtimestamp(ts).strftime("%Y/%m/%dT%H:%M:%S")


def list_action(
    resources: Text,
    tablulate_func,
    format: Text,
    page_size: int,
    page_token: str,
    local_mode: bool,
    resource_ids=[],
):
    metadata = Metadata(local_mode)

    msgs, next_page_token = getattr(metadata.store, "get_%s" % resources)(
        page_size=page_size, page_token=page_token, resource_ids=resource_ids
    )

    if not format:
        if not msgs:
            click.echo("no resources found")
        else:
            headers, contents = tablulate_func(msgs)
            click.echo(tabulate(contents, headers=headers))
            if next_page_token:
                click.echo("next_page_token: %s" % next_page_token)
    else:
        msg = {
            "experiments": [json_format.MessageToDict(msg) for msg in msgs],
            "next_page_token": next_page_token,
        }

        if format == "json":
            click.echo(json.dumps(msg))
        elif format == "yaml":
            click.echo(yaml.dump(msg))
        else:
            raise RuntimeError("format %s unsupported" % format)
