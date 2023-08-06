from typing import Text, List
from argo.workflows import client

from argo.workflows.client.models import (
    V1Container,
    V1EnvVar,
    V1EnvVarSource,
    V1ObjectFieldSelector,
    V1alpha1Arguments,
    V1alpha1Artifact,
    V1alpha1DAGTask,
    V1alpha1DAGTemplate,
    V1alpha1Parameter,
    V1alpha1Template,
    V1alpha1Inputs,
    V1alpha1UserContainer,
    V1alpha1ScriptTemplate,
)
from kubernetes.client.models import V1Volume
from bmlx.utils import naming_utils


# bmlx 里面 一个 component 对应一个node，一个node 对应一个 argo的template，同时对应一个 dag template 中的dag task
class ArgoNode(object):
    def __init__(
        self,
        name: Text,
        image: Text,
        command: Text,
        args: List[Text] = [],
        metrics=None,
    ):
        if not naming_utils.is_valid_argo_name(name):
            raise ValueError(
                "Invalid argo name %s for template, name should be match with pattern %s",
                name,
                naming_utils.argo_name_pattern(),
            )

        self._container = V1Container(image=image, command=[command], args=args)
        self._template: V1alpha1Template = V1alpha1Template(
            name=name, metrics=metrics
        )
        self._template.container = self._container

        self.add_env_variable(
            V1EnvVar(
                name="ARGO_POD_NAME",
                value_from=V1EnvVarSource(
                    field_ref=V1ObjectFieldSelector(
                        api_version="v1", field_path="metadata.name"
                    )
                ),
            )
        )

        self._dag_task = V1alpha1DAGTask(
            name=name, template=self._template.name, dependencies=[]
        )

    @property
    def name(self):
        return self._template.name

    @property
    def container(self):
        return self._container

    def add_env_variable(self, env_variable):
        if not isinstance(env_variable, V1EnvVar):
            raise ValueError(
                "invalid argument. Must be of instance `V1EnvVar`."
            )
        if self._container.env is None:
            self._container.env = []
        self._container.env.append(env_variable)

    def add_dependency(self, node):
        if not isinstance(node, ArgoNode):
            raise ValueError("depends_on should input Node parameters")
        if node.name in self._dag_task.dependencies:
            raise RuntimeError(
                "Duplicated depends, node %s depends on node %s for multiple times"
                % (self.name, node.name)
            )
        self._dag_task.dependencies.append(node.name)

    def set_node_selector(self, node_selector):
        self._template.node_selector = node_selector

    def set_init_containers(self, init_containers):
        if not isinstance(init_containers, List[V1alpha1UserContainer]):
            raise ValueError(
                "set_inputs should input List[V1alpha1UserContainer] parameters"
            )
        self._template.init_containers = init_containers

    def set_inputs(self, inputs):
        if not isinstance(inputs, V1alpha1Inputs):
            raise ValueError(
                "set_inputs should input V1alpha1Inputs parameters"
            )
        self._template.inputs = inputs

    def set_parallelism(self, parallelism):
        self._template.parallelism = parallelism

    def add_volume(self, vol):
        if not isinstance(vol, V1Volume):
            raise ValueError("add_volume should input V1Volume parameters")
        self._template.volumes.append(vol)

    def set_script(self, script):
        if not isinstance(script, V1alpha1ScriptTemplate):
            raise ValueError(
                "set_script should input V1alpha1ScriptTemplate parameters"
            )
        self._template.script = script

    @property
    def template(self):
        return self._template

    @property
    def dag_task(self):
        return self._dag_task
