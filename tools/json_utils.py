import json
from typing import Any, Dict, List, Optional, Set, Union


class JsonUtils:
    @staticmethod
    def object_to_json(data: Any) -> Optional[str]:
        try:
            return json.dumps(data)
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def json_to_pojo(json_str: str, cls: type) -> Any:
        """将JSON字符串转换为Python对象"""
        return json.loads(json_str)

    @staticmethod
    def json_to_list(json_data: str, bean_type) -> Optional[List]:
        try:
            return json.loads(json_data)
        except Exception as e:
            print(e)
            return None
