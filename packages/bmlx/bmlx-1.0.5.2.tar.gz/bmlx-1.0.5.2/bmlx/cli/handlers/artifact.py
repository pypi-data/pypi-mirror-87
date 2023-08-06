import click
import json
import yaml

from datetime import datetime
from typing import Text, Optional, List
from bmlx.proto.metadata import artifact_pb2
from bmlx.metadata.metadata import Metadata
from tabulate import tabulate
from google.protobuf import json_format


def list(
    local_mode: Optional[bool] = False,
    format: Optional[Text] = None,
    resource_ids: Optional[List[int]] = None,
    page_size: Optional[int] = None,
    page_token: Optional[str] = None,
):
    metadata = Metadata(local_mode=local_mode)
    artifacts = metadata.store.get_artifact_list()

    if not format:
        headers = ["name", "ns", "type", "exe_id", "uri", "state"]
        c = tabulate(
            [
                (
                    artifact.name,
                    artifact.namespace,
                    artifact.type,
                    artifact.pipeline_execution_id,
                    artifact.uri,
                    artifact_pb2.Artifact.State.Name(artifact.state),
                )
                for artifact in artifacts
            ],
            headers=headers,
        )
        click.echo(c)
    else:
        d = [json_format.MessageToDict(artifact) for artifact in artifacts]
        if format == "json":
            click.echo(json.dumps(d))
        elif format == "yaml":
            click.echo(yaml.dump(d))
        else:
            raise RuntimeError("unsupported encoding error: %s" % format)


def describe(artifact_ids: List[int], is_local: Optional[bool] = False):
    metadata = Metadata(is_local)

    artifacts = metadata.store.get_artifacts_by_id(artifact_ids)
    tpl = """
Id: {id}
Name: {name}
Type: {type}
Uri: {uri}
Producer: {producer}
Create Timestamp: {create_at}
"""
    click.echo(
        "\n---".join(
            [
                tpl.format(
                    id=artifact.id,
                    name=artifact.name,
                    type=artifact.type,
                    uri=artifact.uri,
                    producer=artifact.producer_component,
                    create_at=datetime.fromtimestamp(
                        artifact.create_timestamp
                    ).strftime("%Y-%m-%d %H:%M:%S"),
                )
                for artifact in artifacts
            ]
        )
    )
