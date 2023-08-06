import collections
import re
from typing import Any, Dict, List, TypeVar, Union, Callable, Optional, Sequence
from kubernetes.client import V1Toleration, V1Affinity
from kubernetes.client.models import (
    V1Container,
    V1EnvVar,
    V1EnvFromSource,
    V1SecurityContext,
    V1Probe,
    V1ResourceRequirements,
    V1VolumeDevice,
    V1VolumeMount,
    V1ContainerPort,
    V1Lifecycle,
    V1Volume,
)

T = TypeVar("T")


def as_string_list(
    list_or_str: Optional[Union[Any, Sequence[Any]]]
) -> List[str]:
    """Convert any value except None to a list if not already a list."""
    if list_or_str is None:
        return None
    if isinstance(list_or_str, Sequence) and not isinstance(list_or_str, str):
        list_value = list_or_str
    else:
        list_value = [list_or_str]
    return [str(item) for item in list_value]


def create_and_append(current_list: Union[List[T], None], item: T) -> List[T]:
    """Create a list (if needed) and appends an item to it."""
    current_list = current_list or []
    current_list.append(item)
    return current_list


class ContainerOp(V1Container):
    """
    A wrapper over k8s container definition object (io.k8s.api.core.v1.Container),
    which is used to represent the `container` property in argo's workflow
    template (io.argoproj.workflow.v1alpha1.Template).

    `Container` class also comes with utility functions to set and update the
    the various properties for a k8s container definition.

    NOTE: A notable difference is that `name` is not required and will not be
    processed for `Container` (in contrast to `V1Container` where `name` is a
    required property).

    See:
    - https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_container.py
    - https://github.com/argoproj/argo/blob/master/api/openapi-spec/swagger.json


    Example:

      from bmlx.execution.bmlxflow.container_op import ContainerOp
      from kubernetes.client.models import V1EnvVar


      # creates a operation
      op = ContainerOp(name='bash-ops',
                       image='busybox:latest',
                       command=['echo'],
                       arguments=['$MSG'])

      op.add_env_variable(V1EnvVar(name='MSG', value='hello world'))

    """

    """
    Attributes:
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    # remove `name` from attribute_map, swagger_types and openapi_types so `name` is not generated in the JSON

    if hasattr(V1Container, "swagger_types"):
        swagger_types = {
            key: value
            for key, value in V1Container.swagger_types.items()
            if key != "name"
        }
    if hasattr(V1Container, "openapi_types"):
        openapi_types = {
            key: value
            for key, value in V1Container.openapi_types.items()
            if key != "name"
        }
    attribute_map = {
        key: value
        for key, value in V1Container.attribute_map.items()
        if key != "name"
    }

    def __init__(
        self, image: str, command: List[str], args: List[str], **kwargs
    ):
        """Creates a new instance of `Container`.

        Args:
            image {str}: image to use, e.g. busybox:latest
            command {List[str]}: entrypoint array.  Not executed within a shell.
            args {List[str]}: arguments to entrypoint.
            **kwargs: keyword arguments for `V1Container`
        """
        # set name to '' if name is not provided
        # k8s container MUST have a name
        # argo workflow template does not need a name for container def
        if not kwargs.get("name"):
            kwargs["name"] = ""

        super(ContainerOp, self).__init__(
            image=image, command=command, args=args, **kwargs
        )

    def _validate_memory_string(self, memory_string):
        """Validate a given string is valid for memory request or limit."""
        if (
            re.match(
                r"^[0-9]+(E|Ei|P|Pi|T|Ti|G|Gi|M|Mi|K|Ki){0,1}$", memory_string
            )
            is None
        ):
            raise ValueError(
                "Invalid memory string. Should be an integer, or integer followed "
                'by one of "E|Ei|P|Pi|T|Ti|G|Gi|M|Mi|K|Ki"'
            )

    def _validate_cpu_string(self, cpu_string):
        "Validate a given string is valid for cpu request or limit."
        if re.match(r"^[0-9]+m$", cpu_string) is not None:
            return

        try:
            float(cpu_string)
        except ValueError:
            raise ValueError(
                "Invalid cpu string. Should be float or integer, or integer followed "
                'by "m".'
            )

    def _validate_positive_number(self, str_value, param_name):
        "Validate a given string is in positive integer format."
        try:
            int_value = int(str_value)
        except ValueError:
            raise ValueError(
                "Invalid {}. Should be integer.".format(param_name)
            )

        if int_value <= 0:
            raise ValueError("{} must be positive integer.".format(param_name))

    def add_resource_limit(self, resource_name, value):
        """Add the resource limit of the container.

        Args:
          resource_name: The name of the resource. It can be cpu, memory, etc.
          value: The string value of the limit.
        """

        self.resources = self.resources or V1ResourceRequirements()
        self.resources.limits = self.resources.limits or {}
        self.resources.limits.update({resource_name: value})
        return self

    def add_resource_request(self, resource_name, value):
        """Add the resource request of the container.

        Args:
          resource_name: The name of the resource. It can be cpu, memory, etc.
          value: The string value of the request.
        """

        self.resources = self.resources or V1ResourceRequirements()
        self.resources.requests = self.resources.requests or {}
        self.resources.requests.update({resource_name: value})
        return self

    def set_memory_request(self, memory):
        """Set memory request (minimum) for this operator.

        Args:
          memory: a string which can be a number or a number followed by one of
                  "E", "P", "T", "G", "M", "K".
        """

        self._validate_memory_string(memory)
        return self.add_resource_request("memory", memory)

    def set_memory_limit(self, memory):
        """Set memory limit (maximum) for this operator.

        Args:
          memory: a string which can be a number or a number followed by one of
                  "E", "P", "T", "G", "M", "K".
        """
        self._validate_memory_string(memory)
        return self.add_resource_limit("memory", memory)

    def set_cpu_request(self, cpu):
        """Set cpu request (minimum) for this operator.

        Args:
          cpu: A string which can be a number or a number followed by "m", which means 1/1000.
        """

        self._validate_cpu_string(cpu)
        return self.add_resource_request("cpu", cpu)

    def set_cpu_limit(self, cpu):
        """Set cpu limit (maximum) for this operator.

        Args:
          cpu: A string which can be a number or a number followed by "m", which means 1/1000.
        """

        self._validate_cpu_string(cpu)
        return self.add_resource_limit("cpu", cpu)

    def set_gpu_limit(self, gpu, vendor="nvidia"):
        """Set gpu limit for the operator. This function add '<vendor>.com/gpu' into resource limit.
        Note that there is no need to add GPU request. GPUs are only supposed to be specified in
        the limits section. See https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/.

        Args:
          gpu: A string which must be a positive number.
          vendor: Optional. A string which is the vendor of the requested gpu. The supported values
            are: 'nvidia' (default), and 'amd'.
        """

        self._validate_positive_number(gpu, "gpu")
        if vendor != "nvidia" and vendor != "amd":
            raise ValueError("vendor can only be nvidia or amd.")

        return self.add_resource_limit("%s.com/gpu" % vendor, gpu)

    def add_volume_mount(self, volume_mount):
        """Add volume to the container

        Args:
          volume_mount: Kubernetes volume mount
          For detailed spec, check volume mount definition
          https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_volume_mount.py
        """

        if not isinstance(volume_mount, V1VolumeMount):
            raise ValueError(
                "invalid argument. Must be of instance `V1VolumeMount`."
            )

        self.volume_mounts = create_and_append(self.volume_mounts, volume_mount)
        return self

    def add_volume_devices(self, volume_device):
        """
        Add a block device to be used by the container.

        Args:
          volume_device: Kubernetes volume device
          For detailed spec, volume device definition
          https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_volume_device.py
        """

        if not isinstance(volume_device, V1VolumeDevice):
            raise ValueError(
                "invalid argument. Must be of instance `V1VolumeDevice`."
            )

        self.volume_devices = create_and_append(
            self.volume_devices, volume_device
        )
        return self

    def add_env_variable(self, env_variable):
        """Add environment variable to the container.

        Args:
          env_variable: Kubernetes environment variable
          For detailed spec, check environment variable definition
          https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_env_var.py
        """

        if not isinstance(env_variable, V1EnvVar):
            raise ValueError(
                "invalid argument. Must be of instance `V1EnvVar`."
            )

        self.env = create_and_append(self.env, env_variable)
        return self

    def add_env_from(self, env_from):
        """Add a source to populate environment variables int the container.

        Args:
          env_from: Kubernetes environment from source
          For detailed spec, check environment from source definition
          https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_env_var_source.py
        """

        if not isinstance(env_from, V1EnvFromSource):
            raise ValueError(
                "invalid argument. Must be of instance `V1EnvFromSource`."
            )

        self.env_from = create_and_append(self.env_from, env_from)
        return self

    def set_image_pull_policy(self, image_pull_policy):
        """Set image pull policy for the container.

        Args:
          image_pull_policy: One of `Always`, `Never`, `IfNotPresent`.
        """
        if image_pull_policy not in ["Always", "Never", "IfNotPresent"]:
            raise ValueError(
                "Invalid imagePullPolicy. Must be one of `Always`, `Never`, `IfNotPresent`."
            )

        self.image_pull_policy = image_pull_policy
        return self

    def add_port(self, container_port):
        """Add a container port to the container.

        Args:
          container_port: Kubernetes container port
          For detailed spec, check container port definition
          https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_container_port.py
        """

        if not isinstance(container_port, V1ContainerPort):
            raise ValueError(
                "invalid argument. Must be of instance `V1ContainerPort`."
            )

        self.ports = create_and_append(self.ports, container_port)
        return self

    def set_security_context(self, security_context):
        """Set security configuration to be applied on the container.

        Args:
          security_context: Kubernetes security context
          For detailed spec, check security context definition
          https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_security_context.py
        """

        if not isinstance(security_context, V1SecurityContext):
            raise ValueError(
                "invalid argument. Must be of instance `V1SecurityContext`."
            )

        self.security_context = security_context
        return self

    def set_stdin(self, stdin=True):
        """
        Whether this container should allocate a buffer for stdin in the container
        runtime. If this is not set, reads from stdin in the container will always
        result in EOF.

        Args:
          stdin: boolean flag
        """

        self.stdin = stdin
        return self

    def set_stdin_once(self, stdin_once=True):
        """
        Whether the container runtime should close the stdin channel after it has
        been opened by a single attach. When stdin is true the stdin stream will
        remain open across multiple attach sessions. If stdinOnce is set to true,
        stdin is opened on container start, is empty until the first client attaches
        to stdin, and then remains open and accepts data until the client
        disconnects, at which time stdin is closed and remains closed until the
        container is restarted. If this flag is false, a container processes that
        reads from stdin will never receive an EOF.

        Args:
          stdin_once: boolean flag
        """

        self.stdin_once = stdin_once
        return self

    def set_termination_message_path(self, termination_message_path):
        """
        Path at which the file to which the container's termination message will be
        written is mounted into the container's filesystem. Message written is
        intended to be brief final status, such as an assertion failure message.
        Will be truncated by the node if greater than 4096 bytes. The total message
        length across all containers will be limited to 12kb.

        Args:
          termination_message_path: path for the termination message
        """
        self.termination_message_path = termination_message_path
        return self

    def set_termination_message_policy(self, termination_message_policy):
        """
        Indicate how the termination message should be populated. File will use the
        contents of terminationMessagePath to populate the container status message
        on both success and failure. FallbackToLogsOnError will use the last chunk
        of container log output if the termination message file is empty and the
        container exited with an error. The log output is limited to 2048 bytes or
        80 lines, whichever is smaller.

        Args:
          termination_message_policy: `File` or `FallbackToLogsOnError`
        """
        if termination_message_policy not in ["File", "FallbackToLogsOnError"]:
            raise ValueError(
                "terminationMessagePolicy must be `File` or `FallbackToLogsOnError`"
            )
        self.termination_message_policy = termination_message_policy
        return self

    def set_tty(self, tty=True):
        """
        Whether this container should allocate a TTY for itself, also requires
        'stdin' to be true.

        Args:
          tty: boolean flag
        """

        self.tty = tty
        return self

    def set_readiness_probe(self, readiness_probe):
        """
        Set a readiness probe for the container.

        Args:
          readiness_probe: Kubernetes readiness probe
          For detailed spec, check probe definition
          https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_probe.py
        """

        if not isinstance(readiness_probe, V1Probe):
            raise ValueError("invalid argument. Must be of instance `V1Probe`.")

        self.readiness_probe = readiness_probe
        return self

    def set_liveness_probe(self, liveness_probe):
        """
        Set a liveness probe for the container.

        Args:
          liveness_probe: Kubernetes liveness probe
          For detailed spec, check probe definition
          https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_probe.py
        """

        if not isinstance(liveness_probe, V1Probe):
            raise ValueError("invalid argument. Must be of instance `V1Probe`.")

        self.liveness_probe = liveness_probe
        return self

    def set_lifecycle(self, lifecycle):
        """
        Setup a lifecycle config for the container.

        Args:
          lifecycle: Kubernetes lifecycle
          For detailed spec, lifecycle definition
          https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_lifecycle.py
        """

        if not isinstance(lifecycle, V1Lifecycle):
            raise ValueError(
                "invalid argument. Must be of instance `V1Lifecycle`."
            )

        self.lifecycle = lifecycle
        return self
