from typing import Text
from bmlx.cli.handlers.utils import format_time, list_action


def list(
    format: Text,
    page_size: int,
    page_token: str,
    local_mode: bool,
    resource_ids=[],
):
    def _f(experiments):
        return (
            ["id", "name", "ctime", "description",],
            [
                (
                    experiment.id,
                    experiment.name,
                    format_time(experiment.create_time),
                    experiment.description,
                )
                for experiment in experiments
            ],
        )

    list_action(
        resources="experiments",
        tablulate_func=_f,
        format=format,
        page_size=page_size,
        page_token=page_token,
        local_mode=local_mode,
        resource_ids=resource_ids,
    )
