import json
from typing import Any, List, Optional


class JsonUtils:
    @staticmethod
    def object_to_json(data: Any) -> Optional[str]:
        try:
            return json.dumps(data)
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def json_to_pojo(json_str: str, cls: type = None) -> Any:
        """将JSON字符串转换为Python对象"""
        # cls参数保留用于未来扩展
        _ = cls  # 避免pylint警告
        return json.loads(json_str)

    @staticmethod
    def json_to_list(json_data: str, bean_type=None) -> Optional[List]:
        try:
            # bean_type参数保留用于未来扩展
            _ = bean_type  # 避免pylint警告
            return json.loads(json_data)
        except Exception as e:
            print(e)
            return None
