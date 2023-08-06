import sys
from bmlx.utils.import_utils import import_func_from_source
from bmlx.execution.runner import Runner


def run_component(
    ctx,
    experiment_id,
    component_id,
    execution_name,
    component_parameters,
    sub_component,
):
    """
    run component directly, this is useful in distribute environment
    """
    create_pipeline_func = import_func_from_source(
        ctx.project.pipeline_path, "create_pipeline"
    )
    pipeline = create_pipeline_func(ctx)

    component = None
    for comp in pipeline.components:
        if comp.id == component_id:
            component = comp
            break

    if component is None:
        raise RuntimeError(
            "unknown component id %s in %s"
            % (component_id, pipeline.components)
        )
    pipeline_execution = ctx.metadata.get_or_create_pipeline_execution(
        pipeline=pipeline,
        experiment_id=experiment_id,
        execution_name=execution_name,
        parameters=component_parameters,
    )
    
    if not pipeline_execution:
        raise RuntimeError("pipeline execution invalid")

    connector = ['/', ''][ctx.project.artifact_storage_base[-1] == '/']
    ctx.project.artifact_storage_base += "%s%s/%s/%s/%s/" % (
        connector,
        str(ctx.env),
        str(pipeline_execution.experiment_id),
        str(pipeline_execution.id),
        str(component.id),
    )

    Runner.launch_component(
        context=ctx,
        pipeline=pipeline,
        pipeline_execution=pipeline_execution,
        component=component,
        extra_parameters=component_parameters,
        sub_component=sub_component,
    )
