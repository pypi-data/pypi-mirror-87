import abc
import string
import logging
import random
import os
from datetime import datetime

from six import with_metaclass
from bmlx.flow.artifact import Artifact
from bmlx.flow.pipeline import Pipeline
from bmlx.flow.component import Component
from bmlx.flow import Channel
from typing import Text, Dict, List, Any, Optional, Tuple

from bmlx.metadata.kubeflow_store import KubeflowStore
from bmlx.proto.metadata import execution_pb2, artifact_pb2
from bmlx.fs.hdfs import HadoopFileSystem

_MAX_RETRY = 3


class Metadata(with_metaclass(abc.ABCMeta)):
    def __init__(
        self, local_mode: bool, local_storage_path: Optional[Text] = None
    ):
        self.store = KubeflowStore(
            local_mode=local_mode, local_storage_path=local_storage_path
        )

    def create_pipeline(self, pipeline: Pipeline, checksum: Text) -> int:
        """
        create new pipeline, this would upload a pipeline to store and store the package to hdfs
        but no execution would created
        NOTE:
        pipeline.meta.manifest should be set here
        """
        return self.store.create_pipeline(
            pipeline_meta=pipeline.meta, checksum=checksum,
        )

    def build_execution_obj(
        self,
        experiment_name: Text,
        pipeline: Pipeline,
        parameters: Dict[Text, Any] = {},
        execution_name: Optional[Text] = None,
        execution_desc: Optional[Text] = None,
    ) -> execution_pb2.Execution:
        experiment = self.store.get_experiment_by_name(
            experiment_name
        ) or self.store.get_experiment_by_id(experiment_name)
        if not experiment:
            raise RuntimeError("unknown experiment id: %s" % experiment)

        execution = execution_pb2.Execution()

        execution.name = execution_name or (
            pipeline.meta.name + self._gen_random_suffix(8)
        )
        execution.description = execution_desc or pipeline.meta.description
        execution.state = execution_pb2.Execution.State.NEW
        # execution.parameters = parameters
        execution.experiment_id = experiment.id
        execution.experiment_context_id = experiment.context_id
        if pipeline.meta.id:
            execution.pipeline_id = pipeline.meta.id
        return execution

    def get_or_create_pipeline_execution(
        self,
        experiment_name: Text,
        pipeline: Pipeline,
        parameters: Dict[Text, Any] = {},
        execution_name: Optional[Text] = None,
        execution_desc: Optional[Text] = None,
    ) -> execution_pb2.Execution:
        execution = self.build_execution_obj(
            experiment_name,
            pipeline,
            parameters,
            execution_name,
            execution_desc,
        )
        return self.store.get_or_create_pipeline_execution(execution)

    def update_pipeline_execution(
        self, execution: execution_pb2.Execution
    ) -> bool:
        return self.store.update_pipeline_execution(execution)

    def get_pipeline_execution_by_id(self, id: int) -> execution_pb2.Execution:
        return self.store.get_pipeline_execution_by_id(id)

    def get_pipeline_execution_by_context_id(
        self, ctx_id: int
    ) -> execution_pb2.Execution:
        return self.store.get_pipeline_execution_by_context_id(ctx_id)

    def get_component_execution(
        self, pipeline_execution: execution_pb2.Execution, component_id: Text,
    ) -> execution_pb2.ComponentExecution:
        return self.store.get_component_execution(
            pipeline_execution, component_id
        )

    def register_component_execution(
        self,
        pipeline: Pipeline,
        pipeline_execution: execution_pb2.Execution,
        component: Component,
        input_artifacts: Optional[List[Artifact]] = [],
        output_artifacts: Optional[List[Artifact]] = [],
    ) -> Tuple[
        execution_pb2.Execution,
        List[artifact_pb2.Artifact],
        List[artifact_pb2.Artifact],
    ]:
        component_execution = execution_pb2.ComponentExecution()
        component_execution.name = f"{pipeline.meta.name}_{pipeline_execution.context_id}_{component.id}"
        component_execution.type = component.id
        component_execution.start_time = int(datetime.now().timestamp())
        component_execution.state = (
            execution_pb2.ComponentExecution.State.RUNNING
        )

        (
            execution_meta,
            inputs,
            outputs,
        ) = self.store.create_or_update_component_execution(
            pipeline_execution=pipeline_execution,
            component_execution=component_execution,
            input_artifacts=[artifact.meta for artifact in input_artifacts],
            pipeline_name=pipeline_execution.name,
        )

        logging.debug(
            "MetaData: registered component_execution: id:%s"
            % execution_meta.id
        )
        return execution_meta, inputs, outputs

    def update_component_execution(
        self,
        pipeline: Pipeline,
        pipeline_execution: execution_pb2.Execution,
        component: Component,
        input_artifacts: Dict[Text, List[Artifact]],
        exec_properties: Dict[Text, Any],
        output_artifacts: List[Artifact],
        state=execution_pb2.ComponentExecution.State.COMPLETED,
    ):
        component_execution = self.store.get_component_execution(
            pipeline_execution=pipeline_execution, component_id=component.id,
        )
        component_execution.finish_time = int(datetime.now().timestamp())
        component_execution.state = state
        # generate fingerprint
        for artifact in output_artifacts:
            artifact.meta.fingerprint = self.generate_artifact_fingerprint(
                input_artifacts=input_artifacts,
                exec_properties=exec_properties,
                component=component,
            )
            logging.info(
                "update_component_execution, generate artifact "
                "fingerprint: %s",
                artifact.meta.fingerprint,
            )

        self.store.create_or_update_component_execution(
            pipeline_execution=pipeline_execution,
            component_execution=component_execution,
            output_artifacts=[artifact.meta for artifact in output_artifacts],
            pipeline_name=pipeline.meta.name,
        )

    def get_artifacts_by_uri(self, uri: Text) -> List[artifact_pb2.Artifact]:
        return self.store.get_artifacts_by_uri(uri)

    def get_artifacts(self) -> List[artifact_pb2.Artifact]:
        return self.store.get_artifacts()

    def publish_artifacts(
        self,
        component_execution: execution_pb2.ComponentExecution,
        pipeline_execution: execution_pb2.Execution,
        artifacts: List[Artifact],
    ) -> int:
        metas = []
        for artifact in artifacts:
            artifact.meta.create_time = int(datetime.now().timestamp())
            artifact.meta.state = artifact_pb2.Artifact.State.LIVE
            metas.append(metas)

        return self.store.create_artifacts(
            component_execution=component_execution,
            pipeline_execution=pipeline_execution,
            artifacts=artifacts,
        )

    # TODO by zhangguanxing, add unittest here
    def get_previous_artifacts(
        self, pipeline_execution: execution_pb2.Execution
    ) -> Dict[Text, List[artifact_pb2.Artifact]]:
        component_executions = self.store.get_component_executions_of_pipeline(
            pipeline_execution=pipeline_execution
        )

        _, outputs = self.store.get_component_executions_artifacts(
            component_executions=component_executions
        )

        ret = {}
        for output in outputs:
            if output.producer_component not in ret:
                ret[output.producer_component] = [output]
            else:
                ret[output.producer_component].append(output)

        return ret

    def generate_artifact_fingerprint(
        self,
        input_artifacts: Dict[Text, List[Artifact]],
        exec_properties: Dict[Text, Any],
        component: Component,
    ) -> Text:
        input_artifacts_arr = sorted(
            [(k, v) for (k, v) in input_artifacts.items()],
            key=lambda ele: ele[0],
        )
        exec_props_arr = sorted(
            [(k, v) for (k, v) in exec_properties.items()],
            key=lambda ele: ele[0],
        )

        return "component: {}#inputs: {}#exec_properties: {}".format(
            component.id,
            ",".join(
                ["{}={}".format(k, repr(v)) for (k, v) in input_artifacts_arr]
            ),
            ",".join(["{}={}".format(k, repr(v)) for (k, v) in exec_props_arr]),
        )

    def get_cached_outputs(
        self,
        input_artifacts: Dict[Text, List[Artifact]],
        exec_properties: Dict[Text, Any],
        component: Component,
        expected_outputs: Dict[Text, Channel],
    ):

        fingerprint = self.generate_artifact_fingerprint(
            input_artifacts, exec_properties, component
        )
        founded_outputs = {}

        for out_name, channel in expected_outputs.items():
            published_artifacts = [
                Artifact(type_name=channel.type_name, meta=artifact)
                for artifact in self.store.get_artifacts(
                    types=[channel.type_name]
                )
                if artifact.fingerprint == fingerprint
            ]
            if published_artifacts:
                founded_outputs[out_name] = published_artifacts

        def compare_outputs(expected_outputs, founded_outputs):
            for k, v in expected_outputs.items():
                if k not in founded_outputs:
                    return False
            return True

        if compare_outputs(expected_outputs, founded_outputs):
            return founded_outputs
        else:
            return {}

    _PKG_PATH = "{pipeline_storage_path}/{experiment}/{package_name}/{checksum}/{package_name}.zip"

    @classmethod
    def upload_package(
        cls,
        pipeline_storage_path: Text,
        experiment: Text,
        local_path: Text,
        checksum: Text,
    ):
        package_name = os.path.splitext(os.path.basename(local_path))[0]
        hdfs = HadoopFileSystem(host=pipeline_storage_path.split("/")[2])
        hdfs_file = cls._PKG_PATH.format(
            pipeline_storage_path=pipeline_storage_path,
            experiment=experiment,
            package_name=package_name,
            checksum=checksum,
        )
        if hdfs.exists(hdfs_file):
            logging.debug(
                "pipeline package %s with checksum %s already exists",
                hdfs_file,
                checksum,
            )
            return hdfs_file

        hdfs.upload(local_path, hdfs_file)
        if not hdfs.exists(hdfs_file):
            raise RuntimeError(
                f"Failed to upload package {local_path} to {hdfs_file}"
            )
        return hdfs_file

    @classmethod
    def download_package(
        cls,
        pipeline_storage_path: Text,
        experiment: Text,
        package_name: Text,
        checksum: Text,
        local_dir: Text,
    ):
        hdfs = HadoopFileSystem(host=pipeline_storage_path.split("/")[2])
        hdfs_file = cls._PKG_PATH.format(
            pipeline_storage_path=pipeline_storage_path,
            experiment=experiment,
            package_name=package_name,
            checksum=checksum,
        )

        if not hdfs.exists(hdfs_file):
            raise RuntimeError(
                f"Package file {hdfs_file} does not exist on hdfs"
            )

        local_file = f"{local_dir}/{package_name}.zip"
        hdfs.download(hdfs_file, local_file)
        return os.path.exists(local_file)

    def _gen_random_suffix(self, N: int):
        return "".join(
            random.choice(string.ascii_uppercase + string.digits)
            for _ in range(N)
        )
