from bmlx.flow import Artifact
from typing import Text, Any, Dict, Optional, List
from bmlx.utils import json_utils


class ExecutionInfo(json_utils.Jsonable):
    def __init__(
        self,
        input_dict: Dict[Text, List[Artifact]],
        output_dict: Dict[Text, List[Artifact]],
        exec_properties: Dict[Text, Any],
        use_cached_result: Optional[bool] = False,
    ):
        self.input_dict = input_dict
        self.output_dict = output_dict
        self.exec_properties = exec_properties
        self.use_cached_result = use_cached_result

    def to_json_dict(self) -> Dict[Text, Any]:
        return {
            "input_dict": self.input_dict,
            "output_dict": self.output_dict,
            "use_cached_result": self.use_cached_result,
        }

    @classmethod
    def from_json_dict(cls, dict_data: Dict[Text, Any]) -> Any:
        return ExecutionInfo(
            input_dict=dict_data["input_dict"],
            output_dict=dict_data["output_dict"],
            exec_properties={},
            use_cached_result=dict_data["use_cached_result"],
        )


class Execution(object):
    pass
