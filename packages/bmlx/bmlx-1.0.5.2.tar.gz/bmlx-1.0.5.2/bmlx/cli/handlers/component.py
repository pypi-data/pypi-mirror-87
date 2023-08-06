import sys
from bmlx.utils.import_utils import import_func_from_source
from bmlx.execution.runner import Runner


def run_component(
    ctx, component_id, execution_name, component_parameters, sub_component
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

    # sub_component 是指 从 pipeline 的 component execution 中分裂出来的子任务，比如
    # xdl 的 scheduler, worker, ps. sub_component 不关心 pipeline 级别的信息，比如meta
    if sub_component:
        pipeline_execution = None
    else:
        pipeline_execution = ctx.metadata.get_or_create_pipeline_execution(
            experiment_name=ctx.experiment,
            pipeline=pipeline,
            execution_name=execution_name,
        )
        if not pipeline_execution:
            raise RuntimeError("pipeline execution invalid")

    Runner.launch_component(
        context=ctx,
        pipeline=pipeline,
        pipeline_execution=pipeline_execution,
        component=component,
        extra_parameters=component_parameters,
        sub_component=sub_component,
    )
