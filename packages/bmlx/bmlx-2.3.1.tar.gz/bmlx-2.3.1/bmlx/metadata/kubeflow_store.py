"""
这个文件废话比较多，这里记录下几个概念方便理解

1. Contexts
ml-metadata里面是通过contexts来串联不同流程的数据的，context和具体的实体(Artifact, Execution 等等)有多对多的关系，context本身也可以多对多
所以在bmlx里面，主要应用了几个context
第一个是 pipeline_run_context
第二个是 component_run_context

2. Type-System
另外ml-metadata底层数据模型的设计，是典型的类型系统设计，每个数据都有Type+Value的组合，所以这里面要不停的处理各种type和数据的映射。比如
artifactType, ExecutionType, ContextType等

3. metaserver的部署
kubeflow的meta包含两个类别，一个是pipelineserver，另外一个是ml-metadata，pipeline server主要维护run, job, experiment等
metaserver主要维护artifact, component execution, events等等，实际上pipeline server的数据，完全也可以放到metaserver中，猜测官方未来也可能会做冗余设计
"""
import os
import logging
import urllib
import requests
import json
import datetime
import itertools
import pathlib
import google.protobuf.descriptor as descriptor

from google.protobuf.message import Message
from ml_metadata.metadata_store import metadata_store
from ml_metadata.proto import metadata_store_pb2 as mlpb
import ml_metadata.errors as mlmd_errors
from typing import Text, List, Optional, Tuple, Dict, Any
from pytz import timezone
from bmlx.bmlx_ini import BmlxINI  # TODO add global varaibe
from bmlx.utils import io_utils, proc_utils
from bmlx.proto.metadata import (
    execution_pb2,
    artifact_pb2,
    pipeline_pb2,
    experiment_pb2,
)

# kubeflow定义的属性
_WORKSPACE_PROPERTY_NAME = "__kf_workspace__"
_RUN_PROPERTY_NAME = "__kf_run__"
_ALL_META_PROPERTY_NAME = "__ALL_META__"

KF_PIPELINE_HOST = "164.90.77.14"  # "www.mlp.bigo.inner" #
KF_PIPELINE_PORT = 8888
KF_META_HOST = "164.90.77.8"
KF_META_PORT = 8889


_DEFAULT_EXPERIMENT_NAME = "Default"
_TIMEOUT = 10


def _retry_handler(f):
    return proc_utils.retry(
        retry_count=3,
        delay=5,
        allowed_exceptions=(mlmd_errors.UnavailableError),
    )(f)


def _http_error_handler(f):
    def _wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except requests.exceptions.HTTPError as e:
            resp = e.response
            raise RuntimeError(
                "call kubeflow api-server error: %s -- %s"
                % (resp.status_code, resp.content)
            )
        except (KeyError, json.JSONDecodeError) as e:
            raise RuntimeError(
                "call kubeflow error [unexpected result]: %s" % str(e)
            )

    return _wrapper


class KubeflowStore(object):
    def whereami(self):
        if (
            "ML_PIPELINE_SERVICE_HOST" in os.environ
            and "ML_PIPELINE_SERVICE_PORT" in os.environ
            and "METADATA_GRPC_SERVICE_SERVICE_HOST" in os.environ
            and "METADATA_GRPC_SERVICE_SERVICE_PORT" in os.environ
        ):
            self._in_kubeflow = True
            self._kf_endpoint = "http://{}:{}".format(
                os.environ["ML_PIPELINE_SERVICE_HOST"],
                os.environ["ML_PIPELINE_SERVICE_PORT"],
            )
            self._kf_metahost = os.environ["METADATA_GRPC_SERVICE_SERVICE_HOST"]
            self._kf_metaport = int(
                os.environ["METADATA_GRPC_SERVICE_SERVICE_PORT"]
            )
        else:
            self._in_kubeflow = False
            self._kf_endpoint = (
                f"http://{KF_PIPELINE_HOST}:{KF_PIPELINE_PORT}/pipeline"
            )
            self._kf_metahost = KF_META_HOST
            self._kf_metaport = KF_META_PORT

    def __init__(self, local_mode=False, local_storage_path=None):
        self.whereami()

        self._rest_session = None
        self._local_mode = local_mode

        if local_mode:
            if not local_storage_path:
                local_storage_path = pathlib.Path(
                    pathlib.Path.home(), ".bmlx", "metadata"
                )
                if not local_storage_path.exists():
                    io_utils.mkdirs(local_storage_path.as_posix())

            sqlite_file = pathlib.Path(local_storage_path, "metadata.db")
            self._ml_store = metadata_store.MetadataStore(
                mlpb.ConnectionConfig(
                    sqlite=mlpb.SqliteMetadataSourceConfig(
                        filename_uri=sqlite_file.as_uri(),
                        connection_mode=mlpb.SqliteMetadataSourceConfig.READWRITE_OPENCREATE,
                    ),
                )
            )
        else:
            self._setup_session()
            self._ml_store = metadata_store.MetadataStore(
                mlpb.MetadataStoreClientConfig(
                    host=self._kf_metahost, port=self._kf_metaport
                )
            )

    def _setup_session(self):
        if self._rest_session:
            return
        self._rest_session = requests.Session()
        ini = BmlxINI()
        if not self._in_kubeflow and (not ini.token or not ini.user):
            raise RuntimeError("please `bmlx login` first")

        self._rest_session.headers.update(
            {"X-Auth-Token": ini.token, "X-Auth-User": ini.user}
        )

    @_http_error_handler
    def _upload_version_package(
        self,
        pipeline_meta: pipeline_pb2.Pipeline,
        local_package: Text,
        version_name: Text,
    ) -> pipeline_pb2.Pipeline:

        if self.get_pipeline_version_by_name(
            pipeline_id=pipeline_meta.id, version_name=version_name
        ):
            raise RuntimeError(
                "pipeline %s, version: %s exists on server"
                % (pipeline_meta.name, version_name)
            )

        params = {
            "pipelineid": pipeline_meta.id,
            "name": version_name,
        }

        resp = self._rest_session.post(
            f"{self._kf_endpoint}/apis/v1beta1/pipelines/upload_version",
            params=params,
            files={"uploadfile": open(local_package, "rb")},
        )

        resp.raise_for_status()
        return _pipeline_version_k2b(json.loads(resp.content), pipeline_meta)

    @_http_error_handler
    def upload_pipeline(
        self,
        pipeline_meta: pipeline_pb2.Pipeline,
        local_package: Text,
        version_name: Text,
    ) -> Text:
        cur_pipeline = self.get_pipeline_by_name(pipeline_meta.name)
        if cur_pipeline:
            return self._upload_version_package(
                cur_pipeline[0], local_package, version_name
            )
        else:
            params = {
                "description": pipeline_meta.description,
                "name": pipeline_meta.name,
                "version_name": version_name,
            }

            resp = self._rest_session.post(
                f"{self._kf_endpoint}/apis/v1beta1/pipelines/upload",
                params=params,
                files={"uploadfile": open(local_package, "rb")},
            )

            resp.raise_for_status()
            return _pipeline_k2b(json.loads(resp.content), pipeline_meta)

    @_http_error_handler
    def _create_pipeline(
        self, pipeline_meta: pipeline_pb2.Pipeline, checksum: Text
    ) -> pipeline_pb2.Pipeline:
        """
        create pipeline is a 'reference' pipeline, which store package in hdfs or external storage
        """
        spec = {
            "name": pipeline_meta.name,
            "description": pipeline_meta.description,
            # "parameters": {""}
            "pipeline_manifest": pipeline_meta.manifest,
            "default_version": {
                "name": checksum,
                "code_source_url": pipeline_meta.uri,
            },
        }

        resp = self._rest_session.post(
            f"{self._kf_endpoint}/apis/v1beta1/pipelines",
            data=json.dumps(spec),
            timeout=_TIMEOUT,
        )

        resp.raise_for_status()
        return _pipeline_k2b(json.loads(resp.content), pipeline_meta)

    def get_previous_artifacts(
        self, pipeline_execution: execution_pb2.Execution
    ) -> Dict[Text, List[artifact_pb2.Artifact]]:
        component_executions = self.get_component_executions_of_pipeline(
            pipeline_execution=pipeline_execution
        )

        _, outputs = self.get_component_executions_artifacts(
            component_executions=component_executions
        )

        ret = {}
        for output in outputs:
            if output.producer_component not in ret:
                ret[output.producer_component] = [output]
            else:
                ret[output.producer_component].append(output)

        return ret

    @_http_error_handler
    def _create_pipeline_version(
        self, pipeline_meta: pipeline_pb2.Pipeline, checksum: Text
    ) -> pipeline_pb2.Pipeline:
        """
        create pipeline is a 'reference' pipeline, which store package in hdfs or external storage
        """
        spec = {
            "resource_references": [
                {
                    "key": {"type": "PIPELINE", "id": pipeline_meta.id,},
                    "relationship": "OWNER",
                }
            ],
            "name": str(checksum),
            # "parameters": {""}
            "pipeline_manifest": pipeline_meta.manifest,
            "code_source_url": pipeline_meta.uri,
        }

        resp = self._rest_session.post(
            f"{self._kf_endpoint}/apis/v1beta1/pipeline_versions",
            data=json.dumps(spec),
            timeout=_TIMEOUT,
        )

        resp.raise_for_status()
        return (json.loads(resp.content), pipeline_meta)

    def create_pipeline(
        self, pipeline_meta: pipeline_pb2.Pipeline, checksum: Text
    ) -> pipeline_pb2.Pipeline:
        """
        kubeflow有两个概念，一个是pipeline，一个是pipeline_version
        """
        cur_pipeline = self.get_pipeline_by_name(pipeline_meta.name)
        logging.debug("got pipeline %s" % pipeline_meta.name)
        if cur_pipeline:
            cur_pipeline = cur_pipeline[0]
            if self.get_pipeline_version_by_name(
                pipeline_id=cur_pipeline.id, version_name=checksum
            ):
                raise RuntimeError(
                    "pipeline %s, version: %s exists on server"
                    % (cur_pipeline.name, checksum)
                )

            pipeline_meta.id = cur_pipeline.id
            cur_pipeline = self._create_pipeline_version(
                pipeline_meta=pipeline_meta, checksum=checksum,
            )
        else:
            cur_pipeline = self._create_pipeline(
                pipeline_meta=pipeline_meta, checksum=checksum,
            )

        return cur_pipeline

    @_http_error_handler
    def create_kfp_pipeline_execution(
        self, execution: execution_pb2.Execution, manifest_generator=None
    ) -> execution_pb2.Execution:
        run = {
            "name": execution.name,
            "description": execution.description,
            "pipeline_spec": {
                "pipeline_id": execution.pipeline_id,
                # "parameters": _pack_parameters(execution.parameters),
            },
            "resource_reference": [
                {
                    "key": {
                        "id": execution.experiment_id,
                        "type": "EXPERIMENT",
                    },
                    "relationship": "OWNER",
                },
                {
                    "key": {
                        "id": execution.context_id,
                        "type": "UNKNOWN_RESOURCE_TYPE",
                    },
                    "relationship": "OWNER",
                },
            ],
        }

        if manifest_generator:
            run["pipeline_spec"]["workflow_manifest"] = json.dumps(
                manifest_generator.gen(execution)
            )

        resp = self._rest_session.post(
            f"{self._kf_endpoint}/apis/v1beta1/runs",
            data=json.dumps(run),
            timeout=_TIMEOUT,
        )

        resp.raise_for_status()
        obj = json.loads(resp.content)
        return _pipeline_execution_k2b(obj["run"])

    @_retry_handler
    def get_or_create_pipeline_execution(
        self, execution: execution_pb2.Execution
    ) -> execution_pb2.Execution:
        previous_context = self._ml_store.get_context_by_type_and_name(
            type_name=_PIPELINE_EXECUTION_CONTEXT_TYPE_NAME,
            context_name=execution.name,
        )

        if not previous_context:
            return self.create_pipeline_execution(execution)
        else:
            logging.info(
                "already created execution context id: %s, type: %s"
                % (previous_context.id, previous_context.type_id)
            )
            execution.context_id = previous_context.id

        return execution

    @_retry_handler
    def create_pipeline_execution(
        self, execution: execution_pb2.Execution
    ) -> execution_pb2.Execution:
        ctx = self._make_mlpb_context(
            context_type=_PIPELINE_EXECUTION_CONTEXT_TYPE_NAME,
            spec=_PIPELINE_EXECUTION_SPEC,
            context_name=execution.name,
            bmlx_pb_msg=execution,
        )
        try:
            [ctx_id] = self._ml_store.put_contexts([ctx])
            execution.context_id = ctx_id
            logging.info(
                "create execution context id: %s, type: %s"
                % (ctx_id, ctx.type_id)
            )
        except mlmd_errors.AlreadyExistsError:
            previous_context = self._ml_store.get_context_by_type_and_name(
                type_name=_PIPELINE_EXECUTION_CONTEXT_TYPE_NAME,
                context_name=execution.name,
            )
            execution.context_id = previous_context.id
        return execution

    @_retry_handler
    def update_pipeline_execution(
        self, execution: execution_pb2.Execution
    ) -> bool:
        previous_context = self._ml_store.get_context_by_type_and_name(
            type_name=_PIPELINE_EXECUTION_CONTEXT_TYPE_NAME,
            context_name=execution.name,
        )
        ctx = self._make_mlpb_context(
            context_type=_PIPELINE_EXECUTION_CONTEXT_TYPE_NAME,
            spec=_PIPELINE_EXECUTION_SPEC,
            context_name=execution.name,
            bmlx_pb_msg=execution,
        )
        ctx.id = previous_context.id
        try:
            [ctx_id] = self._ml_store.put_contexts([ctx])
            execution.context_id = ctx_id
            logging.info(
                "update pipeline execution context id: %s, type: %s successfully!"
                % (ctx_id, ctx.type_id)
            )
            return True
        except mlmd_errors.AlreadyExistsError:
            logging.warning("update pipeline execution, already exit error!")
            return False

    _PIPELINE_NAME_FORMAT = "{pipeline_name}_{pipeline_context_id}"

    @_retry_handler
    def create_or_update_component_execution(
        self,
        pipeline_execution: execution_pb2.Execution,
        component_execution: execution_pb2.ComponentExecution,
        input_artifacts: Optional[List[artifact_pb2.Artifact]] = [],
        output_artifacts: Optional[List[artifact_pb2.Artifact]] = [],
        exec_properties: Dict[Text, Any] = {},
        pipeline_name: Optional[Text] = None,
    ) -> Tuple[
        execution_pb2.Execution,
        List[artifact_pb2.Artifact],
        List[artifact_pb2.Artifact],
    ]:

        if not pipeline_execution.context_id:
            raise RuntimeError("pipeline exectuion context_id invalid")
        contexts = []
        contexts.append(
            self._ml_store.get_contexts_by_id([pipeline_execution.context_id])[
                0
            ]
        )
        component_execution.type_id = self._create_or_update_component_execution_type(
            component_id=component_execution.type,
            exec_properties=exec_properties,
        )
        component_execution_context = self._make_mlpb_context(
            context_type=_COMPONENT_EXECUTION_CONTEXT_TYPE_NAME,
            spec=_COMPONENT_EXECUTION_SPEC,
            context_name=self._get_component_execution_context_name(
                pipeline_execution=pipeline_execution,
                component_id=component_execution.type,
            ),
            bmlx_pb_msg=component_execution,
        )
        existed_ctx = self._ml_store.get_context_by_type_and_name(
            _COMPONENT_EXECUTION_CONTEXT_TYPE_NAME,
            component_execution_context.name,
        )
        if existed_ctx:
            component_execution_context.id = existed_ctx.id
        artifact_events = []
        mlpb_execution = _component_execution_b2m(
            component_execution, workspace_name=pipeline_name
        )
        pipeline_name = self._PIPELINE_NAME_FORMAT.format(
            pipeline_name=pipeline_execution.name,
            pipeline_context_id=pipeline_execution.context_id,
        )

        for input_artifact in input_artifacts:
            input_artifact.type_id = self._create_or_update_artifact_type(
                type_name=input_artifact.type
            )
            existed_artifact = self._ml_store.get_artifact_by_type_and_name(
                input_artifact.type, input_artifact.name
            )
            if existed_artifact:
                input_artifact.id = existed_artifact.id

            artifact_event = (
                _artifact_b2m(
                    input_artifact,
                    pipeline_name=pipeline_name,
                    execution_name=component_execution.name,
                ),
                mlpb.Event(type=mlpb.Event.INPUT),
            )
            artifact_events.append(artifact_event)

        for output_artifact in output_artifacts:
            output_artifact.type_id = self._create_or_update_artifact_type(
                type_name=output_artifact.type
            )

            # output_artifact 可能是已经publish过的artifact，则给artifact.id
            # 赋值,不用重新create
            same_uri_artifacts = self.get_artifacts_by_uri(output_artifact.uri)
            if same_uri_artifacts:
                target = max(same_uri_artifacts, key=lambda m: m.id)
                if target.fingerprint == output_artifact.fingerprint:
                    output_artifact.id = target.id
            else:
                existed_artifact = self._ml_store.get_artifact_by_type_and_name(
                    output_artifact.type, output_artifact.name
                )
                if existed_artifact:
                    output_artifact.id = existed_artifact.id

            artifact_event = (
                _artifact_b2m(
                    output_artifact,
                    pipeline_name=pipeline_name,
                    execution_name=component_execution.name,
                ),
                mlpb.Event(type=mlpb.Event.OUTPUT),
            )

            artifact_events.append(artifact_event)

        try:
            exe_id, input_ids, output_ids = self._ml_store.put_execution(
                execution=mlpb_execution,
                artifact_and_events=artifact_events,
                contexts=contexts + [component_execution_context],
            )
        except mlmd_errors.AlreadyExistsError:
            # same execution has executed, so reuse context
            # get former context
            context_name = self._get_component_execution_context_name(
                pipeline_execution=pipeline_execution,
                component_id=component_execution.type,
            )
            former_context = self._ml_store.get_context_by_type_and_name(
                type_name=_COMPONENT_EXECUTION_CONTEXT_TYPE_NAME,
                context_name=context_name,
            )

            [former_execution] = self._ml_store.get_executions_by_context(
                context_id=former_context.id
            )

            mlpb_execution.id = former_execution.id
            exe_id, input_ids, output_ids = self._ml_store.put_execution(
                execution=mlpb_execution,
                artifact_and_events=artifact_events,
                contexts=contexts,
            )

        return self.get_component_execution_by_id(exe_id)

    @_retry_handler
    def create_artifacts(
        self,
        artifacts: List[artifact_pb2.Artifact],
        component_execution: Optional[execution_pb2.ComponentExecution] = None,
        pipeline_execution: Optional[execution_pb2.Execution] = None,
    ) -> List[int]:
        pipeline_name = None
        execution_name = None

        if pipeline_execution:
            pipeline_name = self._PIPELINE_NAME_FORMAT.format(
                pipeline_name=pipeline_execution.name,
                pipeline_context_id=pipeline_execution.context_id,
            )
        if component_execution:
            execution_name = component_execution.name

        pub = []
        for artifact in artifacts:
            artifact.type_id = self._create_or_update_artifact_type(
                artifact.type
            )
            mlpb_artifact = _artifact_b2m(
                execution_name=execution_name,
                artifact=artifact,
                pipeline_name=pipeline_name,
            )
            pub.append(artifact)

        return self._ml_store.put_artifacts([mlpb_artifact])

    @_http_error_handler
    def _list_actions(
        self,
        resource_name: Text,
        page_size: int = 10,
        page_token: Text = "",
        resource_identifier: Tuple[Text, Text] = None,
        resource_ref_identifier: Tuple[Text, Text] = None,
        resource_ids: List[Text] = [],
        filter_names: List[Text] = [],
    ):
        predicates = []
        for filter_name in filter_names:
            predicates.append(
                {"key": "name", "op": "EQUALS", "string_value": filter_name}
            )

        for filter_id in resource_ids:
            predicates.append(
                {"key": "id", "op": "EQUALS", "string_value": filter_id,}
            )

        params = {
            "filter": urllib.parse.quote(
                json.dumps({"predicates": predicates,})
            ),
            "page_size": page_size,
            "page_token": page_token,
            "sort_by": "created_at desc",
        }

        if resource_identifier:
            params["resource_key.type"] = resource_identifier[0]
            params["resource_key.id"] = resource_identifier[1]

        if resource_ref_identifier:
            params["resource_reference_key.type"] = resource_ref_identifier[0]
            params["resource_reference_key.id"] = resource_ref_identifier[1]

        resp = self._rest_session.get(
            f"{self._kf_endpoint}/apis/v1beta1/%s" % (resource_name),
            params=params,
            timeout=_TIMEOUT,
        )

        if resp.status_code == 404:
            return None, None
        elif resp.status_code != 200:
            raise RuntimeError(
                "unexpected server error [%s]: %s"
                % (resp.status_code, resp.content)
            )
        obj = json.loads(resp.content)
        return obj, obj.get("next_page_token", None)

    def get_pipelines(
        self,
        page_size: int = 10,
        page_token: Text = "",
        resource_ids: List[Text] = [],
        filter_names: List[Text] = [],
    ):
        obj, page_token = self._list_actions(
            resource_name="pipelines",
            page_size=page_size,
            page_token=page_token,
            resource_ids=resource_ids,
            filter_names=filter_names,
        )

        if not obj:
            return [], None
        else:
            return [_pipeline_k2b(p) for p in obj["pipelines"]], page_token

    def get_pipeline_versions(
        self,
        page_size: int = 10,
        page_token: Text = "",
        resource_ids: List[Text] = [],
        filter_names: List[Text] = [],
    ):
        if not resource_ids:
            raise RuntimeError("please set pipeline id")
        if len(resource_ids) > 1:
            raise RuntimeError("only one pipeline id accept")

        obj, page_token = self._list_actions(
            resource_name="pipeline_versions",
            page_size=page_size,
            resource_identifier=("PIPELINE", resource_ids[0]),
            page_token=page_token,
            filter_names=filter_names,
        )

        if not obj:
            return [], None
        else:
            return [(p) for p in obj["versions"]], page_token

    def get_pipeline_by_name(self, name):
        ret = self.get_pipelines(filter_names=[name])
        if ret:
            return ret[0]
        else:
            return None

    def get_pipeline_version_by_name(self, pipeline_id, version_name):
        obj = self.get_pipeline_versions(
            resource_ids=[pipeline_id], filter_names=[version_name]
        )
        if obj:
            return obj[0]
        else:
            return None

    @_retry_handler
    def _get_pipeline_execution_context(
        self, ctx_id
    ) -> execution_pb2.Execution:
        ctx = self._ml_store.get_contexts_by_id([ctx_id])
        if not ctx:
            return None
        else:
            return _pipeline_execution_context_m2b(ctx[0])

    @_retry_handler
    def _get_pipeline_executions_by_experiment(
        self, experiment: experiment_pb2.Experiment
    ) -> List[execution_pb2.Execution]:
        executions = self._ml_store.get_contexts_by_type(
            type_name=_PIPELINE_EXECUTION_CONTEXT_TYPE_NAME
        )

        return [
            _pipeline_execution_context_m2b(exe)
            for exe in executions
            if exe.properties["experiment_context_id"].int_value
            == experiment.context_id
        ]

    def get_pipeline_executions(
        self,
        page_size: int = 10,
        page_token: Text = "",
        resource_ids: List[Text] = [],
        filter_names: List[Text] = [],
        context_ids: List[Text] = [],
        experiment_name: Optional[Text] = _DEFAULT_EXPERIMENT_NAME,
    ) -> Tuple[List[execution_pb2.Execution], Text]:
        experiment = self.get_experiment_by_name(experiment_name)
        if not experiment:
            raise RuntimeError("unfound experiment name: %s" % experiment_name)

        if (
            self._local_mode or context_ids
        ):  # use context means fetch from ml-metadata
            executions = self._get_pipeline_executions_by_experiment(experiment)
            if resource_ids:
                executions = [e for e in executions if e.id in resource_ids]
            if filter_names:
                executions = [e for e in executions if e.name in filter_names]
            if context_ids:
                executions = [
                    e for e in executions if e.context_id in context_ids
                ]

            return executions, None
        else:
            obj, page_token = self._list_actions(
                "runs",
                page_size=page_size,
                page_token=page_token,
                resource_ref_identifier=("EXPERIMENT", experiment.id),
                filter_names=filter_names,
            )

            if not obj:
                return None, None
            else:
                return (
                    [_pipeline_execution_k2b(p) for p in obj["runs"]],
                    page_token,
                )

    def get_pipeline_execution_by_id(
        self, pipeline_execution_id: int
    ) -> execution_pb2.Execution:
        ret, _ = self.get_pipeline_executions(
            resource_ids=[pipeline_execution_id]
        )
        if not ret:
            return None
        else:
            return ret[0]

    def get_pipeline_execution_by_context_id(
        self, ctx_id: int
    ) -> execution_pb2.Execution:
        ret, _ = self.get_pipeline_executions(context_ids=[ctx_id])
        if not ret:
            return None
        else:
            return ret[0]

    @_retry_handler
    def _get_local_experiments(
        self, resource_ids=[], filter_names=[]
    ) -> List[experiment_pb2.Experiment]:
        contexts = self._ml_store.get_contexts_by_type(
            _EXPERIMENT_CONTEXT_TYPE_NAME
        )
        default_context = None
        for context in contexts:
            if context.name == _DEFAULT_EXPERIMENT_NAME:
                default_context = context
                break
        if not default_context:
            default_exp = experiment_pb2.Experiment(
                name=_DEFAULT_EXPERIMENT_NAME, description="defualt experiment",
            )

            default_exp_ctx = self._make_mlpb_context(
                context_type=_EXPERIMENT_CONTEXT_TYPE_NAME,
                spec=_EXPERIMENT_SPEC,
                context_name=_DEFAULT_EXPERIMENT_NAME,
                bmlx_pb_msg=default_exp,
            )

            [default_exp_ctx.id] = self._ml_store.put_contexts(
                [default_exp_ctx]
            )
            contexts.append(default_exp_ctx)

        # 因为这个方法experiment很少，所以直接全拿了过滤
        if resource_ids:
            contexts = [e for e in contexts if e.id in resource_ids]
        if filter_names:
            contexts = [e for e in contexts if e.name in filter_names]

        return [_experiment_m2b(context) for context in contexts]

    def get_experiments(
        self,
        page_size: int = 10,
        page_token: Text = "",
        resource_ids: List[Text] = [],
        filter_names: List[Text] = [],
    ) -> List[experiment_pb2.Experiment]:
        if self._local_mode:
            return (
                self._get_local_experiments(
                    resource_ids=resource_ids, filter_names=filter_names
                ),
                None,
            )
        else:
            obj, page_token = self._list_actions(
                "experiments",
                page_size=page_size,
                page_token=page_token,
                resource_ids=resource_ids,
                filter_names=filter_names,
            )

            if not obj:
                return None, None
            else:
                return (
                    [_experiment_k2b(p) for p in obj["experiments"]],
                    page_token,
                )

    def get_experiment_by_name(self, experiment_name):
        obj, _ = self.get_experiments(filter_names=[experiment_name])
        if obj:
            return obj[0]
        # create experiment
        return self.create_experiment(experiment_name, "")

    @_http_error_handler
    def create_experiment(
        self, experiment_name, experiment_description
    ) -> experiment_pb2.Experiment:
        spec = {"name": experiment_name, "description": experiment_description}
        resp = self._rest_session.post(
            f"{self._kf_endpoint}/apis/v1beta1/experiments",
            data=json.dumps(spec),
            timeout=_TIMEOUT,
        )

        obj = json.loads(resp.content)
        return _experiment_k2b(obj["experiment"])

    def get_experiment_by_id(self, experiment_id):
        obj, _ = self.get_experiments(resource_ids=[experiment_id])
        if obj:
            return obj[0]
        return None

    @_retry_handler
    def get_artifacts_by_types(
        self, types: List[Text] = [],
    ):
        if not types:
            artifacts = self._ml_store.get_artifacts()
        else:
            artifacts = list(
                itertools.chain(
                    *[self._ml_store.get_artifacts_by_type(t) for t in types]
                )
            )

        return [_artifact_m2b(artifact) for artifact in artifacts]

    @_retry_handler
    def get_artifacts_by_id(
        self, ids: List[int]
    ) -> List[artifact_pb2.Artifact]:
        return [
            _artifact_m2b(artifact)
            for artifact in self._ml_store.get_artifacts_by_id(ids)
        ]

    @_retry_handler
    def get_artifacts_by_uri(
        self, uris: List[Text]
    ) -> List[artifact_pb2.Artifact]:
        return [
            _artifact_m2b(artifact)
            for artifact in self._ml_store.get_artifacts_by_uri(uris)
        ]

    @_retry_handler
    def get_component_executions_artifacts(
        self, component_executions: List[execution_pb2.ComponentExecution]
    ) -> Tuple[List[artifact_pb2.Artifact], List[artifact_pb2.Artifact]]:

        events = self._ml_store.get_events_by_execution_ids(
            [
                component_execution.id
                for component_execution in component_executions
            ]
        )

        artifacts = {
            artifact.id: artifact
            for artifact in self._ml_store.get_artifacts_by_id(
                [event.artifact_id for event in events]
            )
        }

        return (
            [
                _artifact_m2b(artifacts[event.artifact_id])
                for event in events
                if event.type == mlpb.Event.INPUT
            ],
            [
                _artifact_m2b(artifacts[event.artifact_id])
                for event in events
                if event.type == mlpb.Event.OUTPUT
            ],
        )

    @_retry_handler
    def get_component_executions_of_pipeline(
        self, pipeline_execution: execution_pb2.Execution
    ) -> List[execution_pb2.ComponentExecution]:
        if not pipeline_execution.context_id:
            raise RuntimeError("unknown pipeline execution")

        return [
            _component_execution_m2b(o)
            for o in self._ml_store.get_executions_by_context(
                pipeline_execution.context_id
            )
        ]

    @_retry_handler
    def get_component_execution(
        self, pipeline_execution: execution_pb2.Execution, component_id: Text,
    ) -> execution_pb2.ComponentExecution:
        if not pipeline_execution.context_id:
            raise RuntimeError("unknown pipeline execution")

        component_executions = self._ml_store.get_executions_by_context(
            pipeline_execution.context_id
        )
        for component_execution in component_executions:
            bmlx_exe = _component_execution_m2b(component_execution)
            if bmlx_exe.type == component_id:
                return bmlx_exe
        return None

    def update_component_execution_run_context(
        component_execution: execution_pb2.ComponentExecution,
        run_context: Dict[Text, Text] = {},
    ):
        pass

    @_retry_handler
    def get_component_execution_by_id(
        self, id: int
    ) -> Tuple[
        execution_pb2.Execution,
        List[artifact_pb2.Artifact],
        List[artifact_pb2.Artifact],
    ]:
        ret = self._ml_store.get_executions_by_id([id])
        if not ret:
            return None, None, None
        else:
            r = self.get_component_executions_artifacts(ret)
            return (_component_execution_m2b(ret[0]), r[0], r[1])

    @_retry_handler
    def _make_mlpb_context_type(self, type_name, spec) -> int:
        try:
            context_type = self._ml_store.get_context_type(type_name=type_name)
            # check properties consistency
            if spec != context_type.properties:
                logging.info(
                    "context type %s schema update, try to update to newer one"
                    % type_name
                )
                self._ml_store.put_context_type(
                    mlpb.ContextType(
                        name=type_name, properties=spec, id=context_type.id,
                    ),
                    can_add_fields=True,
                )
            context_type_id = context_type.id

        except mlmd_errors.NotFoundError:
            context_type_id = self._ml_store.put_context_type(
                mlpb.ContextType(name=type_name, properties=spec,),
                can_add_fields=True,
            )
        return context_type_id

    def _make_mlpb_context(
        self,
        context_type: Text,
        spec: Dict[Text, Any],
        context_name: Text,
        bmlx_pb_msg: Message,
    ) -> mlpb.Context:
        context_type_id = self._make_mlpb_context_type(
            type_name=context_type, spec=spec
        )
        ret = mlpb.Context(name=context_name, type_id=context_type_id,)

        _pack_to_properties(msg=bmlx_pb_msg, properties=ret.properties)
        return ret

    def _get_component_execution_context_name(
        self, pipeline_execution: execution_pb2.Execution, component_id: Text
    ):
        return f"{pipeline_execution.context_id}_{component_id}"

    @_retry_handler
    def _create_or_update_component_execution_type(
        self, component_id: Text, exec_properties: Dict[Text, Any]
    ) -> int:
        try:
            ret = self._ml_store.get_execution_type(type_name=component_id)
        except mlmd_errors.NotFoundError:
            nt = mlpb.ExecutionType(
                name=component_id, properties=_COMPONENT_EXECUTION_SPEC,
            )
            self._ml_store.put_execution_type(
                execution_type=nt, can_add_fields=True
            )
            ret = self._ml_store.get_execution_type(type_name=component_id)
        return ret.id

    @_retry_handler
    def _create_or_update_artifact_type(self, type_name: Text) -> int:
        try:
            ret = self._ml_store.get_artifact_type(type_name=type_name)
            if ret.properties != _ARTIFACT_SPEC:
                logging.info(
                    "detect artifact properties update, update to %s"
                    % _ARTIFACT_SPEC
                )
                return self._ml_store.put_artifact_type(
                    mlpb.ArtifactType(
                        id=ret.id, name=type_name, properties=_ARTIFACT_SPEC
                    ),
                    can_add_fields=True,
                    can_delete_fields=True,
                )
            return ret.id
        except mlmd_errors.NotFoundError:
            nt = mlpb.ArtifactType(name=type_name, properties=_ARTIFACT_SPEC)
            return self._ml_store.put_artifact_type(
                artifact_type=nt, can_add_fields=True
            )


def _pack_parameters(s: str):
    if s:
        d = json.loads(s)
        return [{"key": k, "value": v} for k, v in d.items()]
    return {}


def _parse_time(timestr):
    return int(
        datetime.datetime.strptime(timestr, "%Y-%m-%dT%H:%M:%SZ")
        .replace(tzinfo=timezone("utc"))
        .astimezone()
        .timestamp()
    )


def _parse_status(status_str: Text):
    if status_str == "Running":
        return execution_pb2.State.RUNNING
    elif status_str == "Failed":
        return execution_pb2.State.FAILED
    elif status_str == "Completed":
        return execution_pb2.State.SUCCEEDED
    else:
        logging.warning("unrecogonize status: %s" % status_str)
        return execution_pb2.State.UNKNOWN


def _pipeline_version_k2b(
    obj, tpl: Optional[pipeline_pb2.PipelineVersion] = None
) -> pipeline_pb2.PipelineVersion:
    ret = pipeline_pb2.Pipeline()
    if tpl:
        ret.CopyFrom(tpl)

    ret.id = obj["id"]
    ret.name = obj["name"]
    ret.create_time = _parse_time(obj["created_at"])
    return ret


def _pipeline_k2b(
    obj, tpl: Optional[pipeline_pb2.Pipeline] = None
) -> pipeline_pb2.Pipeline:
    ret = pipeline_pb2.Pipeline()
    if tpl:
        ret.CopyFrom(tpl)
    ret.id = obj["id"]
    ret.name = obj["name"]
    ret.description = obj.get("description", "")
    ret.create_time = _parse_time(obj["created_at"])
    if "default_version" in obj:
        ret.default_version.id = obj["default_version"]["id"]
        ret.default_version.name = obj["default_version"]["name"]
        ret.default_version.create_time = _parse_time(
            obj["default_version"]["created_at"]
        )

        if "parameters" in obj["default_version"]:
            for o in obj["default_version"]["parameters"]:
                if "value" in o:
                    ret.default_version.parameters[o["name"]] = o["value"]

    return ret


def _experiment_k2b(
    obj, tpl: Optional[experiment_pb2.Experiment] = None
) -> experiment_pb2.Experiment:
    ret = experiment_pb2.Experiment()
    if tpl:
        ret.CopyFrom(tpl)

    ret.id = obj["id"]
    ret.name = obj["name"]
    ret.description = obj.get("description", "")
    ret.create_time = _parse_time(obj["created_at"])
    return ret


def _pipeline_execution_k2b(run_obj) -> execution_pb2.Execution:
    execution = execution_pb2.Execution(
        id=run_obj["id"],
        name=run_obj["name"],
        create_time=_parse_time(run_obj["created_at"]),
        schedule_time=_parse_time(run_obj["scheduled_at"]),
        finish_time=_parse_time(run_obj["finished_at"]),
    )
    if "status" in run_obj:
        execution.state = _parse_status(run_obj["status"])

    for ref in run_obj.get("resource_references") or []:
        if ref["key"]["type"] == "EXPERIMENT":
            execution.experiment_id = ref["key"]["id"]
        if ref["key"]["type"] == "PIPELINE_VERSION":
            execution.pipeline_version_id = ref["key"]["id"]
        if (
            ref["key"]["type"] == "UNKNOWN_RESOURCE_TYPE"
            and ref["name"] == "context"
        ):
            execution.context_id = ref["key"]["id"]

    return execution


# 注意，ml-metadata里面实现虽然声明了name/state等字段, 但是很多并没有存，所以最好的方式是优先使用properties里面的数据恢复


def _artifact_m2b(artifact: mlpb.Artifact) -> artifact_pb2.Artifact:
    """
    convert ml-metadata artifact to bmlx artifact
    """
    ret = artifact_pb2.Artifact()
    _unpack_from_properties(msg=ret, properties=artifact.properties)

    ret.id = artifact.id
    ret.uri = artifact.uri
    ret.type_id = artifact.type_id

    return ret


def _artifact_b2m(
    artifact: artifact_pb2.Artifact,
    execution_name: Optional[Text] = None,
    pipeline_name: Optional[Text] = None,
) -> mlpb.Artifact:
    ret = mlpb.Artifact()

    # NOTE, mlmetadata use proto2, so set to zero is not right
    if artifact.id:
        ret.id = artifact.id
    ret.name = artifact.name
    if not ret.name:
        ret.name = artifact.uri
    ret.uri = artifact.uri
    ret.state = artifact.state
    ret.type = artifact.type
    if artifact.type_id:
        ret.type_id = artifact.type_id

    _pack_to_properties(msg=artifact, properties=ret.properties)
    if pipeline_name:
        ret.custom_properties[
            _WORKSPACE_PROPERTY_NAME
        ].string_value = pipeline_name
        ret.custom_properties[_RUN_PROPERTY_NAME].string_value = execution_name

    return ret


def _pipeline_execution_context_m2b(
    execution: mlpb.Context,
) -> execution_pb2.Execution:
    ret = execution_pb2.Execution()

    _unpack_from_properties(msg=ret, properties=execution.properties)

    ret.context_id = execution.id
    return ret


def _component_execution_m2b(
    execution: mlpb.Execution,
) -> execution_pb2.ComponentExecution:
    ret = execution_pb2.ComponentExecution()

    _unpack_from_properties(msg=ret, properties=execution.properties)

    ret.id = execution.id
    ret.type_id = execution.type_id

    return ret


def _component_execution_b2m(
    component_execution: execution_pb2.ComponentExecution, workspace_name=None
) -> mlpb.Execution:
    ret = mlpb.Execution()

    if component_execution.id:
        ret.id = component_execution.id
    ret.name = component_execution.name
    ret.type_id = component_execution.type_id
    ret.last_known_state = component_execution.state

    _pack_to_properties(msg=component_execution, properties=ret.properties)
    if workspace_name:
        ret.custom_properties[
            _WORKSPACE_PROPERTY_NAME
        ].string_value = workspace_name
        ret.custom_properties[_RUN_PROPERTY_NAME].string_value = ret.name

    return ret


def _experiment_m2b(ctx: mlpb.Context) -> experiment_pb2.Experiment:
    ret = experiment_pb2.Experiment()
    _unpack_from_properties(msg=ret, properties=ctx.properties)

    ret.context_id = ctx.id
    return ret


"""
下面三个方法是把bmlx的proto映射成ml-metadata的元数据
"""


def _unpack_from_properties(msg, properties):
    desc = msg.DESCRIPTOR

    for k in properties:
        v = properties[k]
        field_desc = desc.fields_by_name[k]

        if field_desc.label == descriptor.FieldDescriptor.LABEL_REPEATED:
            raise NotImplementedError(
                "repeated filed not support, consider use string instead"
            )
        else:
            if (
                field_desc.type == descriptor.FieldDescriptor.TYPE_FLOAT
                or field_desc.type == descriptor.FieldDescriptor.TYPE_DOUBLE
            ):
                setattr(msg, field_desc.name, v.double_value)
            elif (
                field_desc.type == descriptor.FieldDescriptor.TYPE_STRING
                or field_desc.type == descriptor.FieldDescriptor.TYPE_BYTES
            ):
                setattr(msg, field_desc.name, v.string_value)
            elif (
                field_desc.type == descriptor.FieldDescriptor.TYPE_FIXED32
                or field_desc.type == descriptor.FieldDescriptor.TYPE_FIXED64
                or field_desc.type == descriptor.FieldDescriptor.TYPE_INT32
                or field_desc.type == descriptor.FieldDescriptor.TYPE_INT64
                or field_desc.type == descriptor.FieldDescriptor.TYPE_SFIXED32
                or field_desc.type == descriptor.FieldDescriptor.TYPE_SFIXED64
                or field_desc.type == descriptor.FieldDescriptor.TYPE_SINT32
                or field_desc.type == descriptor.FieldDescriptor.TYPE_SINT64
                or field_desc.type == descriptor.FieldDescriptor.TYPE_UINT32
                or field_desc.type == descriptor.FieldDescriptor.TYPE_UINT64
                or field_desc.type == descriptor.FieldDescriptor.TYPE_ENUM
                or field_desc.type == descriptor.FieldDescriptor.TYPE_BOOL
            ):
                setattr(msg, field_desc.name, v.int_value)
            elif (
                field_desc.type == descriptor.FieldDescriptor.TYPE_MESSAGE
                or field_desc.type == descriptor.FieldDescriptor.TYPE_GROUP
            ):
                raise NotImplementedError(
                    "submessage or group meta not supported, you could implment as string in app level"
                )


def _pack_to_properties(msg, properties):

    for field_desc in msg.DESCRIPTOR.fields:
        if field_desc.label == descriptor.FieldDescriptor.LABEL_REPEATED:
            pass
            # raise NotImplementedError(
            #     "repeated field not support, use string instead"
            # )
        else:
            if (
                field_desc.type == descriptor.FieldDescriptor.TYPE_FLOAT
                or field_desc.type == descriptor.FieldDescriptor.TYPE_DOUBLE
            ):
                properties[field_desc.name].double_value = getattr(
                    msg, field_desc.name
                )
            elif (
                field_desc.type == descriptor.FieldDescriptor.TYPE_STRING
                or field_desc.type == descriptor.FieldDescriptor.TYPE_BYTES
            ):
                properties[field_desc.name].string_value = getattr(
                    msg, field_desc.name
                )
            elif (
                field_desc.type == descriptor.FieldDescriptor.TYPE_FIXED32
                or field_desc.type == descriptor.FieldDescriptor.TYPE_FIXED64
                or field_desc.type == descriptor.FieldDescriptor.TYPE_INT32
                or field_desc.type == descriptor.FieldDescriptor.TYPE_INT64
                or field_desc.type == descriptor.FieldDescriptor.TYPE_SFIXED32
                or field_desc.type == descriptor.FieldDescriptor.TYPE_SFIXED64
                or field_desc.type == descriptor.FieldDescriptor.TYPE_SINT32
                or field_desc.type == descriptor.FieldDescriptor.TYPE_SINT64
                or field_desc.type == descriptor.FieldDescriptor.TYPE_UINT32
                or field_desc.type == descriptor.FieldDescriptor.TYPE_UINT64
                or field_desc.type == descriptor.FieldDescriptor.TYPE_ENUM
                or field_desc.type == descriptor.FieldDescriptor.TYPE_BOOL
            ):
                properties[field_desc.name].int_value = getattr(
                    msg, field_desc.name
                )
            elif (
                field_desc.type == descriptor.FieldDescriptor.TYPE_MESSAGE
                or field_desc.type == descriptor.FieldDescriptor.TYPE_GROUP
            ):
                raise NotImplementedError(
                    "submessage or group meta not supported, you could implment as string in app level"
                )


def _reflect_properties_from_pb(desc: descriptor.Descriptor):
    ret = {}

    for field_desc in desc.fields:
        if field_desc.label == descriptor.FieldDescriptor.LABEL_REPEATED:
            ret[field_desc.name] = mlpb.STRING
        else:
            if (
                field_desc.type == descriptor.FieldDescriptor.TYPE_FLOAT
                or field_desc.type == descriptor.FieldDescriptor.TYPE_DOUBLE
            ):
                ret[field_desc.name] = mlpb.DOUBLE
            elif (
                field_desc.type == descriptor.FieldDescriptor.TYPE_STRING
                or field_desc.type == descriptor.FieldDescriptor.TYPE_BYTES
            ):
                ret[field_desc.name] = mlpb.STRING
            elif (
                field_desc.type == descriptor.FieldDescriptor.TYPE_FIXED32
                or field_desc.type == descriptor.FieldDescriptor.TYPE_FIXED64
                or field_desc.type == descriptor.FieldDescriptor.TYPE_INT32
                or field_desc.type == descriptor.FieldDescriptor.TYPE_INT64
                or field_desc.type == descriptor.FieldDescriptor.TYPE_SFIXED32
                or field_desc.type == descriptor.FieldDescriptor.TYPE_SFIXED64
                or field_desc.type == descriptor.FieldDescriptor.TYPE_SINT32
                or field_desc.type == descriptor.FieldDescriptor.TYPE_SINT64
                or field_desc.type == descriptor.FieldDescriptor.TYPE_UINT32
                or field_desc.type == descriptor.FieldDescriptor.TYPE_UINT64
                or field_desc.type == descriptor.FieldDescriptor.TYPE_ENUM
                or field_desc.type == descriptor.FieldDescriptor.TYPE_BOOL
            ):
                ret[field_desc.name] = mlpb.INT
            elif field_desc.type == descriptor.FieldDescriptor.TYPE_MESSAGE:
                ret[field_desc.name] = mlpb.STRING
            elif field_desc.type == descriptor.FieldDescriptor.TYPE_GROUP:
                raise NotImplementedError(
                    "submessage or group meta not supported, you could implment as string in app level"
                )

    return ret


_ARTIFACT_SPEC = _reflect_properties_from_pb(artifact_pb2.Artifact.DESCRIPTOR)

_COMPONENT_EXECUTION_SPEC = _reflect_properties_from_pb(
    execution_pb2.ComponentExecution.DESCRIPTOR
)
_PIPELINE_EXECUTION_SPEC = _reflect_properties_from_pb(
    execution_pb2.Execution.DESCRIPTOR
)
_EXPERIMENT_SPEC = _reflect_properties_from_pb(
    experiment_pb2.Experiment.DESCRIPTOR
)

_PIPELINE_EXECUTION_CONTEXT_TYPE_NAME = "bmlx.context.execution"
_COMPONENT_EXECUTION_CONTEXT_TYPE_NAME = "bmlx.context.component_execution"
_EXPERIMENT_CONTEXT_TYPE_NAME = "bmlx.context.experiment"
