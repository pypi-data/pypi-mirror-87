import abc
import logging

from six import with_metaclass
import inspect
from bmlx.flow import (
    Node,
    Pipeline,
    Channel,
    DriverArgs,
    ExecutorClassSpec,
    Artifact,
)
from typing import Dict, Text, Any, cast, List
from bmlx.context import BmlxContext
from bmlx.execution.execution import ExecutionInfo
from bmlx.config import Configuration
from bmlx.proto.metadata import execution_pb2


class Launcher(with_metaclass(abc.ABCMeta)):
    """
    launcher mainly prepare essential environment for components
    """

    def __init__(
        self,
        context: BmlxContext,
        component: Node,
        pipeline: Pipeline,
        driver_args: DriverArgs,
        extra_parameters: Dict[Text, Any] = None,
    ):
        self._component = component
        self._pipeline = pipeline
        self._ctx = context
        self._input_dict = component.inputs
        self._output_dict = component.outputs
        self._driver_args = driver_args
        self._exec_properties = component.exec_properties
        self._load_component_configs()
        if extra_parameters:
            logging.info("updated extra parameters: %s" % extra_parameters)
            # TODO recursive update
            self._exec_properties.update(extra_parameters)

    """
    each component has two level configs
       1. top level is called runtime_configs, this is usally resources/meta and so on
       2. component specified configs, which would passing to component implmentation,
          like hyper parameters, artifact storage path etc.
    """

    def _load_component_configs(self):
        if (
            self._ctx.project
            and self._ctx.project.configs["component_configs"].exists()
        ):
            component_config_view = self._ctx.project.configs["component_configs"]

            if component_config_view[self._component.id].exists():
                logging.debug("loaded configs for %s" % self._component.id)
                self._exec_properties["runtime_configs"] = \
                    component_config_view[self._component.id]

    def run_executor(
        self,
        input_dict: Dict[Text, Channel],
        output_dict: Dict[Text, Channel],
        exec_properties: Dict[Text, Any],
    ):
        """
        in different environment, executor mainly extract
        parameters from command line or distriuted envinronets
        """
        executor_class_spec = cast(
            ExecutorClassSpec, self._component.executor_spec
        )
        executor = executor_class_spec.executor_class(self._ctx)
        executor.execute(input_dict, output_dict, exec_properties)

    def cleanup(
        self, component_execution_state: execution_pb2.ComponentExecution.State
    ) -> Text:
        executor_class_spec = cast(
            ExecutorClassSpec, self._component.executor_spec
        )
        executor = executor_class_spec.executor_class(self._ctx)
        return executor.cleanup(component_execution_state)

    def run_driver(self) -> ExecutionInfo:
        driver = self._component.driver_spec.driver_class(
            metadata=self._ctx.metadata
        )

        logging.info("running driver for %s", self._component.id)
        execution_info = driver.pre_execution(
            input_dict=self._input_dict,
            output_dict=self._output_dict,
            exec_properties=self._exec_properties,
            pipeline=self._pipeline,
            component=self._component,
            driver_args=self._driver_args,
            artifact_base_uri=self._ctx.project.artifact_storage_base,
        )

        return execution_info

    def register_component_execution(
        self, input_dict: Dict[Text, List[Artifact]]
    ):
        input_artifacts = []
        for name, inputs in input_dict.items():
            input_artifacts.extend(inputs)

        logging.info("register input artifacts: %s" % input_artifacts)
        self._ctx.metadata.register_component_execution(
            pipeline=self._pipeline,
            pipeline_execution=self._driver_args.pipeline_execution,
            component=self._component,
            input_artifacts=input_artifacts,
        )

    def publish_component_execution(
        self,
        execution_info: ExecutionInfo,
        state: execution_pb2.ComponentExecution.State,
    ):
        output_artifacts = []
        for name, outputs in execution_info.output_dict.items():
            output_artifacts.extend(outputs)

        logging.info("publish output artifacts: %s" % (output_artifacts))
        self._ctx.metadata.update_component_execution(
            pipeline=self._pipeline,
            pipeline_execution=self._driver_args.pipeline_execution,
            component=self._component,
            input_artifacts=execution_info.input_dict,
            exec_properties=execution_info.exec_properties,
            output_artifacts=output_artifacts,
            state=state,
        )

    def launch(self):
        execution_info = self.run_driver()
        self.register_component_execution(input_dict=execution_info.input_dict)
        state = execution_pb2.ComponentExecution.State.RUNNING
        if execution_info.use_cached_result:
            logging.info("component %s use cached result", self._component.id)
            state = execution_pb2.ComponentExecution.State.CACHED
        else:
            logging.info("execute %s", self._component.id)
            try:
                self.run_executor(
                    execution_info.input_dict,
                    execution_info.output_dict,
                    execution_info.exec_properties,
                )
                state = execution_pb2.ComponentExecution.State.COMPLETED
            except Exception as e:
                logging.exception("unexpected exception in executor")
                state = execution_pb2.ComponentExecution.State.FAILED
                raise RuntimeError(e)

        self.publish_component_execution(
            execution_info=execution_info, state=state
        )
