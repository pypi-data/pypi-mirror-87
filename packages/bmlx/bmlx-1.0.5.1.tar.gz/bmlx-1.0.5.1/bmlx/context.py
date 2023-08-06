import itertools
import logging
import sys
from typing import Text, Dict, Any, Optional
from bmlx.alarm import AlarmManager, Receipt
from bmlx.project_spec import Project
from bmlx.bmlx_ini import BmlxINI
from bmlx.utils.import_utils import import_class_by_path
from bmlx.flow.hook import Hook
from bmlx.alarm import Alarm, Level


class DefaultAlarmHook(Hook):
    def onComponentDone(self, context, pipeline, component, ret):
        if ret.status == Hook.Status.FAIL:
            context.alert_manager.emit_alarms(
                [
                    Alarm(
                        level=Level.WARNING,
                        vars={
                            "message": "execute pipeline %s, component %s error"
                            % (pipeline.meta.name, component.id),
                            "pipeline": pipeline,
                            "context": context,
                        },
                    )
                ]
            )

    def onPipelineDone(self, context, pipeline, ret):
        if ret.status == Hook.Status.FAIL:
            context.alert_manager.emit_alarms(
                [
                    Alarm(
                        level=Level.WARNING,
                        vars={
                            "message": "execute pipeline %s error"
                            % pipeline.meta.name,
                            "pipeline": pipeline,
                            "context": context,
                        },
                    )
                ]
            )


class BmlxContext(object):
    """
    Context shared between all command groups.
    there are two types of fields,
    one is parameters could be changed by commandline, it could be access by ctx.local ctx.hparams
    another is project spec fields, which could be access by ctx.project, such as ctx.project.name
    """

    __slots__ = [
        "local_mode",
        "user",
        "token",
        "project",
        "namespace",
        "owner",
        "dry_run",
        "custom_parameters",
        "debug",
        "engine",
        "experiment",
        "package",
        "checksum",
        "workflow_id",
        "kubeflow_runid",
        "_store",
        "pipeline_storage_base",
        "alert_manager",
        "hooks",
    ]

    def __init__(self):
        self._store = None
        self.project = None
        self.alert_manager = None
        self.hooks = []

    def init(
        self,
        local_mode: Optional[bool] = False,
        namespace: Optional[Text] = None,
        custom_config_file: Optional[Text] = None,
        custom_entry_file: Optional[
            Text
        ] = None,  # 用于强制指定 bmlx run 使用的 pipeline 文件
        custom_parameters: Optional[Dict[Text, Any]] = {},
        dry_run: Optional[bool] = False,
        experiment: Optional[Text] = None,
        debug: Optional[bool] = False,
        engine: Optional[Text] = "kubeflow",
        workflow_id: Optional[Text] = "",
        kubeflow_runid: Optional[Text] = "",
    ):
        self.local_mode = local_mode
        self.project = Project(custom_config_file, custom_entry_file)
        sys.path.append(self.project.base_path)
        self.namespace = (
            namespace or self.project.configs["namespace"].as_str() or "default"
        )
        self.dry_run = dry_run
        self.debug = debug
        self.experiment = (
            experiment
            or self.project.configs["experiment"].as_str()
            or "default"
        )
        self.engine = engine
        self.pipeline_storage_base = self.project.configs["pipeline_config"][
            "pipeline_storage_base"
        ].as_filename()
        self.workflow_id = workflow_id
        self.kubeflow_runid = kubeflow_runid
        self.custom_parameters = custom_parameters
        bmlx_ini = BmlxINI()
        self.user = bmlx_ini.user
        self.token = bmlx_ini.token

        if self.project.configs["alert"].exists():
            self.alert_manager = AlarmManager.load_from_config(
                self.project, self.project.configs["alert"]
            )
            if self.local_mode:
                self.alert_manager.limit_receipt_types(
                    [Receipt.Type.CONSOLE]
                )  # 本地模式只打开本地打印报警，不发邮件和微信
            self.hooks.append(DefaultAlarmHook())

        for hook_path in self.project.configs["hooks"]:
            hook_cls = import_class_by_path(hook_path.as_str())
            if not issubclass(hook_cls, Hook):
                raise RuntimeError(
                    "invalid calss %s, must be subclass of bmlx.flow.pipeline.hook.Hook"
                    % hook_cls
                )
            self.hooks.append(hook_cls())

        # bmlx.yml 中的 parameters 字段中的内容 设置为 custom_parameters
        for k, v in self.project.configs["parameters"].items():
            if k not in self.custom_parameters:
                self.custom_parameters[k] = v.as_str()

    def __str__(self):
        return ", ".join(
            [key + ": " + str(getattr(self, key)) for key in self.__slots__]
        )

    @property
    def metadata(self):
        from bmlx.metadata.metadata import Metadata

        if not self._store:
            self._store = Metadata(self.local_mode)
        return self._store

    def image(self):
        """
        get running image, we would use bmlx image as default
        but user's could override image
        """
        from bmlx import __version__

        return (
            self.project.configs["pipeline_config"]["image"]["name"].as_str(
                "harbor.bigo.sg/mlplat/bmlx:%s" % __version__
            ),
            self.project.configs["pipeline_config"]["image"][
                "pull_secret"
            ].as_str(),
            self.project.configs["pipeline_config"]["image"]["policy"].as_str(
                "Always"
            ),
        )

    def dnsPolicy(self):
        return self.project.configs["pipeline_config"]["dns_policy"].as_str()

    def dnsConfig(self):
        return {
            "nameservers": self.project.configs["pipeline_config"][
                "dns_config"
            ]["nameservers"].as_str_seq(),
        }

    def generate_component_run_command(
        self,
        component_id: Text,
        execution_name: Text,
        entry: Text = None,
        extra: Optional[Dict[Text, Any]] = {},
        collect_log=False,
        sub_component=False,
        need_workflow_inject=False,
    ):
        """
        FOR internal developers:
        custom_arguments shoud be Text:Text Format, you could parse these arguments
        in component/launcher implements
        """
        argv = []
        if collect_log:
            argv = ["log_collector"]
        argv.extend(
            [
                "bmlx_rt",
                "run",
                "--namespace",
                self.namespace,
                "--experiment",
                self.experiment,
                "--entry",
                entry or self.project.pipeline_path,
            ]
        )
        # local run does not need to download package
        if not self.local_mode:
            assert self.checksum
            argv.extend(
                ["--package", self.project.name, "--checksum", self.checksum]
            )
        else:
            argv.extend(["--local"])

        # kubeflow使用argo variable，是可以在argo模板中注入此次运行的唯一id
        # 这个可以方便后期追踪相关任务
        if need_workflow_inject:
            argv.extend(["--workflow_id", "{{workflow.uid}}"])
            argv.extend(["--kubeflow_runid", "{{workflow.runid}}"])

        for k, v in itertools.chain(self.custom_parameters.items()):
            argv.extend(["-P", "{}={}".format(k, v)])

        for k, v in itertools.chain(extra.items()):
            argv.extend(["-T", "{}={}".format(k, v)])

        argv.extend(["-E", execution_name])
        argv.extend([component_id])
        if sub_component:
            argv.append("--sub_component")

        logging.debug("generated command %s" % argv)
        return argv

    def generate_pipeline_cleanup_command(
        self, execution_name: Text, entry: Text = None,
    ):
        argv = []
        argv.extend(
            [
                "bmlx_rt",
                "cleanup",
                "--package",
                self.project.name,
                "--checksum",
                self.checksum,
                "--namespace",
                self.namespace,
                "--experiment",
                self.experiment,
                "--entry",
                entry or self.project.pipeline_path,
                "--workflow_id",
                "{{workflow.uid}}",
                "--kubeflow_runid",
                "{{workflow.runid}}",
                "--workflow_status",
                "{{workflow.status}}",
            ]
        )

        argv.extend(["-E", execution_name])
        logging.debug("generated command %s" % argv)
        return argv
