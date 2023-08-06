from typing import Text
from bmlx.proto.metadata import execution_pb2
from bmlx.cli.handlers.utils import format_time, list_action


def list(
    format: Text,
    page_size: int,
    page_token: str,
    local_mode: bool,
    resource_ids=[],
):
    def _f(executions):
        return (
            ["id", "run_name", "pipeline", "status", "ctime", "stime", "ftime"],
            [
                (
                    exe.id,
                    exe.name,
                    exe.pipeline_version_id,
                    execution_pb2.Execution.State.Name(exe.state),
                    format_time(exe.create_time),
                    format_time(exe.schedule_time),
                    format_time(exe.finish_time),
                )
                for exe in executions
            ],
        )

    list_action(
        resources="pipeline_executions",
        tablulate_func=_f,
        format=format,
        page_size=page_size,
        page_token=page_token,
        local_mode=local_mode,
        resource_ids=resource_ids,
    )
