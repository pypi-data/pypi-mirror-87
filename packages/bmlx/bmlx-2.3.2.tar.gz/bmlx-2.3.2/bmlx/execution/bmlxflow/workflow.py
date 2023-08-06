import yaml
import json
from typing import Text, List, Dict, Any
from argo.workflows import client
from kubernetes.client.models import (
    V1PodDNSConfig,
    V1ObjectMeta,
    V1LocalObjectReference,
)
from argo.workflows.client.models import (
    V1alpha1Workflow,
    V1alpha1WorkflowSpec,
    V1alpha1Template,
    V1alpha1DAGTask,
    V1alpha1DAGTemplate,
    V1alpha1WorkflowStatus,
    V1alpha1Metrics,
)
from bmlx.utils import yaml_utils, naming_utils
from bmlx.execution.bmlxflow import ArgoNode


class Dag(object):
    def __init__(self, name: Text):
        if not naming_utils.is_valid_argo_name(name):
            raise ValueError(
                "Invalid argo name %s for template, name should be match with pattern %s",
                name,
                naming_utils._ARGO_NAMING_RE,
            )
        self._name = name
        self._template = V1alpha1DAGTemplate(tasks=[])

    @property
    def name(self):
        return self._name

    def add_task(self, task: V1alpha1DAGTask):
        if not isinstance(task, V1alpha1DAGTask):
            raise ValueError("add_task should input V1alpha1DAGTask parameter")
        self._template.tasks.append(task)

    @property
    def template(self):
        return self._template


class Workflow(object):
    def __init__(self, name: Text):
        if not naming_utils.is_valid_argo_name(name):
            raise ValueError(
                "Invalid argo name %s for template, name should be match with pattern %s",
                name,
                naming_utils.argo_name_pattern(),
            )
        self._name = name
        self._spec = V1alpha1WorkflowSpec(
            entrypoint=f"{name}-entrypoint", templates=[]
        )
        self._exit_node = None
        self._metrics = None
        self._nodes = []

    def add_node(self, t: ArgoNode):
        if not isinstance(t, ArgoNode):
            raise ValueError("add_node should input Node parameter")
        self._nodes.append(t)

    def set_host_network(self, host_network):
        self._spec.host_network = host_network

    def set_dns_policy(self, policy):
        self._spec.dns_policy = policy

    def set_dns_config(self, config):
        if not isinstance(config, V1PodDNSConfig):
            raise ValueError(
                "set_dns_config should input V1PodDNSConfig parameter"
            )
        self._spec.dns_config = config

    def set_image_pull_secrets(self, secret):
        if not isinstance(secret, List[V1LocalObjectReference]):
            raise ValueError(
                "set_image_pull_secrets should be List[V1LocalObjectReference] parameter"
            )
        self._spec.image_pull_secrets = secret

    def set_node_selector(self, selectors):
        self._sepc.node_selectors = selectors

    def set_exit_handler(self, t: ArgoNode):
        self._exit_node = t

    def set_metrics(self, m: V1alpha1Metrics):
        self._metrics = m

    def arrange_nodes(self):
        if not self._nodes:
            raise RuntimeError("Should add_node before calling arrange_nodes")
        self._spec.templates = []
        dag = Dag(name=self._name)
        for node in self._nodes:
            self._spec.templates.append(node.template)
            dag.add_task(node.dag_task)
        # generate entry point template
        tmplt = V1alpha1Template(
            name=f"{dag.name}-entrypoint", dag=dag.template
        )
        self._spec.templates.append(tmplt)

        if self._exit_node:
            self._spec.templates.append(self._exit_node.template)
            self._spec.on_exit = self._exit_node.name
        if self._metrics:
            self._spec.metrics = self._metrics

    @property
    def workflow(self):
        self.arrange_nodes()
        workflow = V1alpha1Workflow(
            api_version="argoproj.io/v1alpha1",
            kind="Workflow",
            metadata=V1ObjectMeta(name=self._name),
            spec=self._spec,
            status=V1alpha1WorkflowStatus(),
        )
        return workflow

    def compile(self):
        return self.to_json()

    def to_json_dict(self, omitempty=True) -> Dict[str, Any]:
        """Returns the Workflow manifest as a dict.

        :param omitempty: bool, whether to omit empty values
        """
        result = V1alpha1Workflow.to_dict(self.workflow, True)

        if omitempty:
            return yaml_utils.omitempty(result)

        return result

    def to_json(self, omitempty=True, **kwargs) -> str:
        """Returns the Workflow manifest as a YAML."""
        d: Dict[str, Any] = self.to_json_dict(omitempty=omitempty)

        opts = dict(default_flow_style=False)
        opts.update(kwargs)
        serialized = json.dumps(d, indent=2, sort_keys=True)
        return serialized
