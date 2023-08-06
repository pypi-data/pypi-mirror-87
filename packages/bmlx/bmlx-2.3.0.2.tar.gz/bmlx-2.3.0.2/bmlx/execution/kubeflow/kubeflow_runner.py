import os
import sys
import logging
from typing import Text, Optional, List
import tempfile
import yaml
from kfp import compiler, dsl
from kfp.compiler.compiler import _validate_workflow
from kubernetes.client.models import V1SecurityContext

from bmlx.flow import Pipeline
from bmlx.proto.metadata import execution_pb2
from bmlx.execution.runner import Runner
from bmlx.context import BmlxContext
from bmlx.execution.kubeflow.kubeflow_component import KubeflowComponent


class KubeflowManifestGenerator:
    def __init__(
        self,
        ctx: BmlxContext,
        pipeline: Pipeline,
        params: List[dsl.PipelineParam] = [],
    ):
        self._pipeline = pipeline
        self._ctx = ctx
        self._compiler = compiler.Compiler()
        self._params = params

    def _construct_pipeline_graph(
        self, pipeline_execution: Optional[execution_pb2.Execution] = None
    ):
        """Constructs a Kubeflow Pipeline graph.

        Args:
        pipeline_execution: created pipeline execution
        """
        if pipeline_execution:  # create run by 'bmlx run'
            execution_name = pipeline_execution.name
            custom_entry_file = self._ctx.project.pipeline_path
        else:  # in create run on kubeflow page
            execution_name = [
                param
                for param in self._params
                if param.name == "execution_name"
            ][0]
            custom_entry_file = [
                param for param in self._params if param.name == "entry"
            ][0]

        # update the bmlx parameters, so that those parameters will be populated
        # when kubeflow run its pipeline with parameters
        for param in self._params:
            if param.name not in ("execution_name", "entry"):
                self._ctx.custom_parameters[param.name] = param

        bmlx_image, _, policy = self._ctx.image()

        arguments = self._ctx.generate_pipeline_cleanup_command(
            execution_name=execution_name, entry=custom_entry_file
        )

        exit_op = dsl.ContainerOp(
            name="clean_up",
            image=bmlx_image,
            command=arguments[0],
            arguments=arguments[1:],
        )
        exit_op.set_security_context(V1SecurityContext(run_as_user=0))

        with dsl.ExitHandler(exit_op):
            component_to_kfp_op = {}
            for component in self._pipeline.components:
                depends_on = set()
                for upstream_component in component.preorders:
                    depends_on.add(
                        component_to_kfp_op[upstream_component].container_op
                    )

                kubeflow_op = KubeflowComponent(
                    ctx=self._ctx,
                    depends_on=depends_on,
                    bmlx_pipeline=self._pipeline,
                    bmlx_component=component,
                    execution_name=execution_name,
                    entry=custom_entry_file,
                )
                component_to_kfp_op[component] = kubeflow_op

    def _gen_workflow_metrics(self, pipeline_execution):
        def _gen_labels():
            return [
                {
                    "key": "bmlx_pipeline",
                    "value": str(self._pipeline.meta.name),
                },
                {"key": "bmlx_experiment", "value": str(self._ctx.experiment)},
                {
                    "key": "namespace",
                    "value": str(self._pipeline.meta.namespace),
                },
                {"key": "bmlx_workflow_id", "value": "{{workflow.uid}}"},
                {"key": "bmlx_workflow_name", "value": "{{workflow.name}}"},
                {
                    "key": "bmlx_create_time",
                    "value": "{{workflow.creationTimestamp}}",
                },
            ]

        return {
            "prometheus": [
                {
                    "name": "bmlx_pipeline_execution_time",
                    "help": "execution time of bmlx pipeline %s"
                    % self._pipeline.meta.name,
                    "labels": _gen_labels(),
                    "gauge": {"value": r"{{workflow.duration}}"},
                },
                {
                    "name": "bmlx_pipeline_fail",
                    "help": "status of pipeline execution",
                    "labels": _gen_labels(),
                    "when": r"{{workflow.status}} == Failed",
                    "counter": {"value": "1"},
                },
                {
                    "name": "bmlx_pipeline_success",
                    "help": "status of pipeline execution",
                    "labels": _gen_labels(),
                    "when": r"{{workflow.status}} == Succeeded",
                    "counter": {"value": "1"},
                },
            ]
        }

    def gen(self, pipeline_execution):
        logging.info(
            "[KubeflowRuner] compiling pipeline {} package {} checksum {}".format(
                self._pipeline.meta.name,
                self._ctx.project.package,
                self._ctx.checksum,
            )
        )

        def construct_pipeline_graph():
            return self._construct_pipeline_graph(pipeline_execution)

        # Create workflow spec and write out to package.
        workflow = self._compiler._create_workflow(
            pipeline_func=construct_pipeline_graph,
            pipeline_name=self._pipeline.meta.name or self._ctx.project.name,
            params_list=self._params,
        )

        workflow["spec"]["metrics"] = self._gen_workflow_metrics(
            pipeline_execution=pipeline_execution
        )
        workflow["spec"]["hostNetwork"] = True
        workflow["spec"]["hostIPC"] = True
        _validate_workflow(workflow)

        return yaml.safe_load(self._compiler._write_workflow(workflow))


class KubeflowRunner(Runner):
    def __init__(self, pipeline: Pipeline, ctx: BmlxContext):
        if not pipeline:
            raise ValueError("Runner must set pipeline!")

        self._pipeline = pipeline
        self._ctx = ctx
        self._compiler = compiler.Compiler()

    def run(self, execution_name: Text, execution_description: Text) -> None:
        execution = self._ctx.metadata.build_execution_obj(
            experiment_name=self._ctx.experiment,
            pipeline=self._pipeline,
            execution_name=execution_name,
            execution_desc=execution_description,
        )

        execution_info = self._ctx.metadata.store.create_kfp_pipeline_execution(
            execution,
            manifest_generator=KubeflowManifestGenerator(
                ctx=self._ctx, pipeline=self._pipeline,
            ),
        )

        logging.info(
            "created new run in experiment: %s, id: %s, name: %s"
            % (self._ctx.experiment, execution_info.id, execution_info.name,)
        )

    def deploy(self, version_name: Text = "",) -> None:
        pipeline_name, pipeline_checksum = (
            self._ctx.project.name,
            self._ctx.checksum,
        )

        params = [
            dsl.PipelineParam(
                name="execution_name",
                value=f"{pipeline_name}-{pipeline_checksum}-[[ScheduledTime]]-[[Index]]",
            ),
            dsl.PipelineParam(name="entry", value="pipeline.py"),
        ]

        for k, v in self._ctx.custom_parameters.items():
            params.append(dsl.PipelineParam(name=k, value=v))

        manifest_generator = KubeflowManifestGenerator(
            ctx=self._ctx, pipeline=self._pipeline, params=params
        )

        yaml_obj = manifest_generator.gen(None)
        with tempfile.TemporaryDirectory(
            suffix=None, prefix=None, dir=None
        ) as tempdir:
            with open(os.path.join(tempdir, pipeline_name + ".yml"), "w") as fp:
                fp.write(yaml.safe_dump(yaml_obj))
            try:
                self._ctx.metadata.store.upload_pipeline(
                    self._pipeline.meta,
                    fp.name,
                    version_name or pipeline_checksum,
                )
            except Exception as e:
                logging.warning(
                    "Failed with exception %s when upload pipeline to kubeflow",
                    e,
                )
                sys.exit(-1)
            logging.info(
                "Deployed pipeline to kubeflow, "
                "pipeline name: %s, version_name: %s, checksum: %s"
                % (
                    pipeline_name or self._pipeline.meta.name,
                    version_name,
                    pipeline_checksum,
                )
            )
