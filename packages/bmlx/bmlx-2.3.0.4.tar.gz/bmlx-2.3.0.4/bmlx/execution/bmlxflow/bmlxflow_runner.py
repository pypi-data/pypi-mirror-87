import os
import sys
import logging
from typing import Text, Optional, List
import tempfile
import yaml
import socket

from bmlx.flow import Pipeline, Component
from bmlx.context import BmlxContext

from bmlx.execution.runner import Runner
from bmlx.execution.bmlxflow import ArgoNode
from bmlx.execution.bmlxflow import Workflow
from bmlx.utils import naming_utils

from argo.workflows.client.models import (
    V1alpha1MetricLabel,
    V1alpha1Metrics,
    V1alpha1Prometheus,
    V1alpha1Gauge,
    V1alpha1Counter,
)


class BmlxflowRunner(Runner):
    def __init__(self, ctx: BmlxContext, pipeline: Pipeline):
        if not pipeline:
            raise ValueError("Runner must set pipeline!")

        self._pipeline = pipeline
        self._ctx = ctx

    def gen_argo_node(
        self, bmlx_component: Component,
    ):
        arguments = self._ctx.generate_component_run_command(
            component_id=bmlx_component.id,
            execution_name="{{workflow.name}}",
            # 先产生workflow.spec.yml，后上传 package 以及 创建 experiment。
            # 因此这里的 experiment_id 填占位符，在 server端创建experiment的时候，将 experiment_id, package_checksum
            # 设置到argo 的 workflow parameters中.
            # argo 执行时候替换 experiment_id 占位符为实际值
            experiment_id="{{workflow.parameters.experiment_id}}",
            collect_log=True,
            checksum="{{workflow.parameters.package_checksum}}",
            package_uri="{{workflow.parameters.package_uri}}",
        )

        command = arguments[0]
        arguments = arguments[1:]

        bmlx_image, _, policy = self._ctx.image()
        node = ArgoNode(
            name=bmlx_component.id.replace(".", "-").replace(
                "_", "-"
            ),  # k8s 名字有要求
            image=bmlx_image,
            command=command,
            args=arguments,
            metrics=self.gen_template_metrics(type(bmlx_component).__name__),
        )
        node.container.image_pull_policy = policy
        return node

    def gen_exit_node(self):
        arguments = self._ctx.generate_pipeline_cleanup_command(
            execution_name="{{workflow.name}}",
            checksum="{{workflow.parameters.package_checksum}}",
            experiment_id="{{workflow.parameters.experiment_id}}",
            package_uri="{{workflow.parameters.package_uri}}",
        )
        command = arguments[0]
        arguments = arguments[1:]

        bmlx_image, _, policy = self._ctx.image()
        node = ArgoNode(
            name="clean-up", image=bmlx_image, command=command, args=arguments,
        )
        node.container.image_pull_policy = policy
        return node

    def compile_pipeline(self, workflow_name: Text, use_host_network: bool):
        # generate argo workflow spec yml file
        component_to_node = {}
        workflow = Workflow(name=workflow_name)
        workflow.set_host_network(use_host_network)
        workflow.set_exit_handler(self.gen_exit_node())
        workflow.set_metrics(self.gen_workflow_metrics())
        for component in self._pipeline.components:
            node = self.gen_argo_node(component)
            for upstream_component in sorted(
                component.preorders, key=lambda x: x.id
            ):
                node.add_dependency(component_to_node[upstream_component])

            workflow.add_node(node)
            component_to_node[component] = node
        return workflow.compile()

    def gen_workflow_spec(
        self, workflow_name: Text, use_host_network: bool = True
    ):
        workflow_name = workflow_name.replace("_", "-")  # argo 命名要求
        if not naming_utils.is_valid_argo_name(workflow_name):
            raise ValueError(
                "Invalid argo workflow name %s, argo name pattern: %s",
                workflow_name,
                naming_utils.argo_name_pattern(),
            )

        spec = self.compile_pipeline(workflow_name, use_host_network)
        path = os.path.join(self._ctx.project.base_path, ".workflow_spec.json")
        with open(path, "w") as f:
            f.write(spec)

    def gen_template_metrics(self, node_name):
        def _gen_labels():
            return [
                V1alpha1MetricLabel(
                    key="bmlx_pipeline", value=str(self._pipeline.meta.name)
                ),
                V1alpha1MetricLabel(
                    key="bmlx_experiment_name",
                    value="{{workflow.parameters.experiment_name}}",
                ),
                V1alpha1MetricLabel(
                    key="bmlx_experiment_id",
                    value="{{workflow.parameters.experiment_id}}",
                ),
                V1alpha1MetricLabel(
                    key="namespace", value="{{workflow.parameters.namespace}}"
                ),
                V1alpha1MetricLabel(key="node_name", value=node_name,),
            ]

        return V1alpha1Metrics(
            prometheus=[
                V1alpha1Prometheus(
                    name="bmlx_comp_run_duration",
                    help="execution time of bmlx component",
                    labels=_gen_labels(),
                    gauge=V1alpha1Gauge(value="{{duration}}", realtime=True),
                ),
                V1alpha1Prometheus(
                    name="bmlx_comp_run_fail",
                    help="bmlx component run fail counter",
                    labels=_gen_labels(),
                    when="{{status}} == Failed",
                    counter=V1alpha1Counter(value="1"),
                ),
                V1alpha1Prometheus(
                    name="bmlx_comp_run_success",
                    help="bmlx component run success counter",
                    labels=_gen_labels(),
                    when="{{status}} == Succeeded",
                    counter=V1alpha1Counter(value="1"),
                ),
                V1alpha1Prometheus(
                    name="bmlx_comp_run_error",
                    help="bmlx component run error counter",
                    labels=_gen_labels(),
                    when="{{status}} == Error",
                    counter=V1alpha1Counter(value="1"),
                ),
            ]
        )

    def gen_workflow_metrics(self):
        def _gen_labels():
            return [
                V1alpha1MetricLabel(
                    key="bmlx_pipeline", value=str(self._pipeline.meta.name)
                ),
                V1alpha1MetricLabel(
                    key="bmlx_experiment_name",
                    value="{{workflow.parameters.experiment_name}}",
                ),
                V1alpha1MetricLabel(
                    key="bmlx_experiment_id",
                    value="{{workflow.parameters.experiment_id}}",
                ),
                V1alpha1MetricLabel(
                    key="namespace", value="{{workflow.parameters.namespace}}"
                ),
            ]

        return V1alpha1Metrics(
            prometheus=[
                V1alpha1Prometheus(
                    name="bmlx_exp_run_duration",
                    help="execution time of bmlx pipeline",
                    labels=_gen_labels(),
                    gauge=V1alpha1Gauge(
                        value="{{workflow.duration}}", realtime=True
                    ),
                ),
                V1alpha1Prometheus(
                    name="bmlx_exp_run_fail",
                    help="bmlx pipeline execution fail counter",
                    labels=_gen_labels(),
                    when="{{workflow.status}} == Failed",
                    counter=V1alpha1Counter(value="1"),
                ),
                V1alpha1Prometheus(
                    name="bmlx_exp_run_success",
                    help="bmlx pipeline execution success counter",
                    labels=_gen_labels(),
                    when="{{workflow.status}} == Succeeded",
                    counter=V1alpha1Counter(value="1"),
                ),
                V1alpha1Prometheus(
                    name="bmlx_exp_run_error",
                    help="bmlx pipeline execution error counter",
                    labels=_gen_labels(),
                    when="{{workflow.status}} == Error",
                    counter=V1alpha1Counter(value="1"),
                ),
            ]
        )

    # 创建 轻量级 experiment, 这条分支只会出现在 本地run 提交一个bmlx flow pipeline 到 argo workflow
    def run(
        self,
        package_uri: Text,
        package_checksum: Text,
        execution_description: Text,
    ) -> None:
        pipeline_name = self._pipeline.meta.name.replace("_", "-")
        experiment_name = f"light-weight-{pipeline_name}"
        if not naming_utils.is_valid_argo_name(experiment_name):
            raise ValueError(
                "Invalid argo name %s for experiment, name should be match with pattern %s",
                experiment_name,
                naming_utils._ARGO_NAMING_RE,
            )

        # 轻量级的experiment 会立即执行

        def get_parameter_value(v):
            if isinstance(v, dict):
                return str(v["value"])
            else:
                return str(v)

        # 构造参数信息，用于前端显示
        parameters = {
            k: get_parameter_value(v)
            for k, v in self._ctx.project.configurables().items()
        }
        exp = self._ctx.metadata.create_light_weight_experiment(
            name=experiment_name,
            package_uri=package_uri,
            package_checksum=package_checksum,
            dag=self._pipeline.get_pipeline_dag(),  # 填充dag 信息，用于前端显示
            parameters=parameters,
        )
        logging.info(
            "[BmlxflowRunner] created experiment, name: %s, id: %s",
            exp.name,
            exp.id,
        )
