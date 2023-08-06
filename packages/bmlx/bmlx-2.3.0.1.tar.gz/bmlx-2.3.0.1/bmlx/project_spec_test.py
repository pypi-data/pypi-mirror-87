import os
import unittest
import yaml
import tempfile
from bmlx.project_spec import Project


class ProjectSpecTest(unittest.TestCase):
    def testGetConfigurableSuccess(self):
        yaml_content = """
name: demo-pipeline
namespace: mlplat
experiment: Default
description: "demo pipeline for bmlx tutorial"
entry: pipeline.py
configurables:
  bmlx.yml:
    - parameters.*
    - settings.*

# parameters 可能经常变动
parameters:
  fg_conf_path: "hdfs://bigo-rt/user/bmlx/fg/likee-follow/ori_fg.yml"
  sample_uri_base: "hdfs://bigocluster/user/alg_rank/like/trainDataMr/mr_feature_processor_xdl_follow/OTHER/"
  model_uri_base: hdfs://bigo-rt/user/bmlx/checkpoints/demo-pipeline/"
  start_sample_hour: "20200713/20"
  end_sample_hour: ""
  max_input_hours:
    value: 1
    validator: {name: maxmin, parameters: {max: 24, min: 1}}
# settings 一般很少变动，主要是一些使用资源的配置
settings:
  # pipeline 级别的setting
  pipeline:
    image:
      name: harbor.bigo.sg/mlplat/bmlx:0.5.15
        """

        with tempfile.TemporaryDirectory() as tempdir:
            # 跳到临时目录
            os.chdir(tempdir)
            # 创建临时的 pipeline.py
            file_path = os.path.join(tempdir, "pipeline.py")
            with open(file_path, "w") as f:
                f.write("test")
            # 创建 bmlx.yml
            file_path = os.path.join(tempdir, "bmlx.yml")
            with open(file_path, "w") as f:
                f.write(yaml_content)

            project = Project(config_name=file_path)
            configs = project.configurables()
            self.assertEqual(len(configs), 7)
            self.assertTrue("bmlx.settings.pipeline.image.name" in configs)
            self.assertTrue("bmlx.parameters.fg_conf_path" in configs)
