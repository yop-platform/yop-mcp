from mcp.server.fastmcp import FastMCP
from typing import Optional
from tools.http_utils import HttpUtils
from tools.api_md_utils import ApiMdUtils
from pathlib import Path
import json
import os

# 获取当前脚本的绝对路径，并推导项目根目录
current_dir = os.path.dirname(os.path.abspath(__file__))  # [6,7](@ref)
project_root = os.path.dirname(current_dir)  # 假设项目根目录是当前目录的上级
# file_path = os.path.join(project_root, "data", "config.json")  # 动态拼接路径

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


# Create an MCP server
mcp = FastMCP("yop-mcp-server")

# api_ext_info = ""
api_ext_info = read_file("/Users/yp-21022/Develop/Cursor/yop-mcp-server/docs/ext/api_ext.md")



@mcp.tool()
def yeepay_open_platform_overview():
    """
    通过此工具，可以快速了解易宝支付开放平台(YOP)的平台规范，产品介绍，API概览信息

    Returns:
        str: 易宝支付开放平台(YOP)的概览信息(markdown格式)
    """

    return HttpUtils.download_content("https://open.yeepay.com/apis/docs/llms.txt")

# @mcp.tool()
# def open_yepay_com_llms_txt(path: Optional[any] = "/"):
#     """
#     获取open.yeepay.com网站的的llms.txt文件
    
#     Args:
#         path: Optional[str] = "/" - 指定要获取的文件路径，默认为根目录"/"
    
#     Returns:
#         str: 文件内容
#     """

#     # 判断path是否为字符串类型
#     if isinstance(path, str):
#         # 简单检查是否匹配URL格式（以http://或https://开头）
#         if path.startswith("http://") or path.startswith("https://"):
#             print(f"检测到URL: {path}")
    
#     # 这里我们直接返回本地文件，实际应用中可能需要从网站获取
#     return read_file("./docs/llms.txt")

@mcp.tool()
def yeepay_products_and_apis():
    """
    通过此工具，获取易宝支付开放平台(YOP)的产品能力，以及相关的API能力信息

    Returns:
        str: 易宝支付开放平台(YOP)产品能力，以及相关的API能力信息(markdown格式)
    """

    # https://open.yeepay.com/apis/docs/apis/docking-product-tree.json
    return HttpUtils.download_content("https://open.yeepay.com/apis/docs/apis/docking-product-tree.json")

@mcp.tool()
def yeepay_yop_api_definition(apiId: str):
    """
    通过此工具，获取易宝支付(YOP)的API详细定义，包含认证方式、入参、出参、对接示例等信息

    Args:
        apiId: str - API唯一标识
    
    Returns:
        str: API详细定义，包含认证方式、入参、出参、对接示例等信息(markdown格式)
        
    """

    # https://open.yeepay.com/apis/docs/apis/dac023730d434d61bcada629810beb99/definition.json
    return ApiMdUtils.convert_data_to_markdown(json.loads(
        HttpUtils.download_content("https://open.yeepay.com/apis/docs/apis/"+apiId+"/definition.json"))
        ) + "\n\n" + api_ext_info


@mcp.tool()
def yeepay_yop_java_sdk_user_guide():
    """
    通过此工具，获取易宝支付(YOP)的yop-java-sdk使用说明
    
    Returns:
        str: yop-java-sdk使用说明(markdown格式)
        
    """
    try:
        platform_info = json.loads(HttpUtils.download_content("https://open.yeepay.com/apis/commons/doc/platform/info"))
        platform_version = platform_info.get("data").get("docVersion")
        return HttpUtils.download_content("https://open.yeepay.com/apis/docs/platform/"+platform_version+"/sdk_guide/java-sdk-guide.html")
    except Exception:
        return read_file("/Users/yp-21022/Develop/Cursor/yop-mcp-server/docs/sdks/yop-java-sdk-user-guide.md")


# -------------------------------------------------官方示例------------------------------------------
# Add an addition tool
# @mcp.tool()
# def add(a: int, b: int) -> int:
#     """Add two numbers"""
#     return a + b

# Cursor 不支持资源、提示词
# Add a dynamic greeting resource
# @mcp.resource("greeting://{name}")
# def get_greeting(name: str) -> str:
#     """Get a personalized greeting"""
#     return f"Hello, {name}!"

# @mcp.prompt()
# def echo_prompt(message: str) -> str:
#     """Create an echo prompt"""
#     return f"Please process this message: {message}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
