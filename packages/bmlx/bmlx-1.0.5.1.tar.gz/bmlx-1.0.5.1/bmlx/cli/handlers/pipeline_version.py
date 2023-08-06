from typing import Text
from bmlx.cli.handlers.utils import format_time, list_action


def list(
    format: Text,
    page_size: int,
    page_token: str,
    local_mode: bool,
    resource_ids=[],
):
    def _f(pipeline_versions):
        return (
            ["id", "name", "ctime"],
            [
                (
                    pipeline_version.id,
                    pipeline_version.name,
                    format_time(pipeline_version.create_time),
                )
                for pipeline_version in pipeline_versions
            ],
        )

    list_action(
        resources="pipeline_versions",
        tablulate_func=_f,
        format=format,
        page_size=page_size,
        page_token=page_token,
        local_mode=local_mode,
        resource_ids=resource_ids,
    )
