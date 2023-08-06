"""Kubeflow Pipelines based implementation of bmlx components.

These components are lightweight wrappers around the KFP DSL"s ContainerOp,
and ensure that the container gets called with the right set of input
arguments. It also ensures that each component exports named output
attributes that are consistent with those provided by the native bmlx
components, thus ensuring that both types of pipeline definitions are
compatible.
Note: This requires Kubeflow Pipelines SDK to be installed.
"""
import kubernetes as k8s
from typing import Set, Dict, Text
import logging
from kfp import dsl
from kubernetes.client.models import V1SecurityContext

from bmlx.flow import Pipeline as BmlxPipeline
from bmlx.flow import Component as BmlxComponent
from bmlx.context import BmlxContext


_WORKFLOW_ID_KEY = "WORKFLOW_ID"


class KubeflowComponent(object):
    """Base component for all Kubeflow pipelines bmlx components.

    Returns a wrapper around a KFP DSL ContainerOp class, and adds named output
    attributes that match the output names for the corresponding native bmlx
    components.
    """

    def __init__(
        self,
        ctx: BmlxContext,
        depends_on: Set[dsl.ContainerOp],
        bmlx_pipeline: BmlxPipeline,
        bmlx_component: BmlxComponent,
        execution_name=None,
        entry=None,
        file_outputs: Dict[Text, Text] = None,
    ):
        """Creates a new Kubeflow-based component.

        This class essentially wraps a dsl.ContainerOp construct in Kubeflow
        Pipelines.

        Args:
          ctx: BmlxContext with context info
          depends_on: The set of upstream KFP ContainerOp components that this
            component will depend on.
          bmlx_pipeline: pipeline def
          bmlx_component: The logical bmlx component to wrap.
          execution_name: execution name of pipeline execution
          entry: entry point for bmlx, e.g. pipeline.py
          file_outputs: file outputs of kubeflow components
        """
        arguments = ctx.generate_component_run_command(
            component_id=bmlx_component.id,
            execution_name=execution_name,
            entry=entry,
            collect_log=False,
            need_workflow_inject=True,
        )

        command = arguments[0]
        arguments = arguments[1:]

        bmlx_image, _, policy = ctx.image()

        file_outputs = file_outputs or {}
        # add default file-output, refer to
        # https://github.com/kubeflow/pipelines/blob/master/sdk/python/kfp/dsl/_container_op.py#L1004
        file_outputs.update(
            {
                "mlpipeline-ui-metadata": "/mlpipeline-ui-metadata.json",
                "mlpipeline-metrics": "/mlpipeline-metrics.json",
            }
        )

        self.container_op = dsl.ContainerOp(
            name=bmlx_component.id.replace(".", "_"),
            command=command,
            image=bmlx_image,
            arguments=arguments,
            file_outputs=file_outputs,
            pvolumes={
                "/data/corefiles": k8s.client.V1Volume(
                    name="corefiles",
                    host_path=k8s.client.V1HostPathVolumeSource(
                        path="/data/corefiles",
                    ),
                ),
            },
        )
        self.container_op.set_image_pull_policy(policy)
        self.container_op.set_security_context(
            V1SecurityContext(privileged=True, run_as_user=0)
        )

        logging.info(
            "Adding upstream dependencies for component {}, using image: {}, policy: {}".format(
                self.container_op.name, bmlx_image, policy
            )
        )
        for op in depends_on:
            logging.info("   ->  Component: {}".format(op.name))
            self.container_op.after(op)

        self.container_op.add_pod_label("add-pod-env", "true")
        self.container_op.add_pod_label("bmlx_component", bmlx_component.id)
        self.container_op.add_pod_label(
            "bmlx_pipeline", bmlx_pipeline.meta.name
        )
