from mcp.server.fastmcp import FastMCP
from tools.cert_key_parser import parse_certificates
from tools.cert_utils import download_cert, gen_key_pair
from tools.http_utils import HttpUtils
from tools.api_md_utils import ApiMdUtils
import json
import os
from typing import Dict, Any

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


@mcp.tool()
def yeepay_yop_gen_key_pair(algorithm="RSA", format="pkcs8", storage_type="file"):
    """
    根据密钥算法生成非对称加密的密钥对（公钥和私钥），并保存到本地路径
    
    参数:
        algorithm: 密钥算法，可选值为 "RSA" 或 "SM2"，默认为 "RSA"
        format: 密钥格式，可选值为 "pkcs8"或"pkcs1"，默认为 "pkcs8"
        storage_type: 密钥存储类型，"file"或"string"，默认为 "file"
    """
    return gen_key_pair(algorithm=algorithm, format=format, storage_type=storage_type)


@mcp.tool()
def yeepay_yop_download_cert(algorithm: str = "RSA", serial_no: str = "", auth_code: str = "", 
                 private_key: str = "", public_key: str = "", pwd: str = "") -> Dict[str, Any]:
    """
    根据密钥算法、CFCA证书的序列号、授权码、非对称密钥对（公钥和私钥）、密码，下载该证书，并保存到本地路径
    
    Args:
        algorithm: 密钥算法，可选值为 "RSA" 或 "SM2"，默认为 "RSA"
        serial_no: cfca证书序列号
        auth_code: cfca证书授权码
        private_key: Base64 编码后的私钥字符串
        public_key: Base64 编码后的公钥字符串
        pwd: 密码，长度：12~16位
        
    Returns:
        Dict包含:
        - message: 响应信息
        - pfxCert: 私钥证书路径(.pfx)
        - pubCert: 公钥证书路径(.cer)
    """
    return download_cert(algorithm=algorithm, serial_no=serial_no, auth_code=auth_code, private_key=private_key, public_key=public_key, pwd=pwd)

@mcp.tool()
def yeepay_yop_parse_certificates(algorithm="RSA", pfxCert=None, pubCert=None, pwd=None):
    """
    根据证书文件解析出Base64编码后的公钥或私钥字符串
    
    Args:
        algorithm (str): 密钥算法，可选值为 "RSA" 或 "SM2"，默认为 "RSA"
        pfxCert (str): 私钥证书（.pfx）文件路径
        pubCert (str): 公钥证书（.cer）文件路径
        pwd (str, optional): PFX证书的密码，默认为None
    
    Returns:
        dict: 包含解析结果的字典，格式如下:
            {
                'message': 响应信息,
                'privateKey': Base64编码后的私钥字符串,
                'publicKey': Base64编码后的公钥字符串
            }
    """
    return parse_certificates(algorithm=algorithm, pfxCert=pfxCert, pubCert=pubCert, pwd=pwd)


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
    # 生成密钥对
    # print(yeepay_yop_gen_key_pair(algorithm="SM2", format="pkcs8", storage_type="file"))

    # 下载证书
    # serial_no = "4928999747"
    # auth_code = "64NPRSS6AR"
    # private_key = "MIGEAgEAMBAGByqGSM49AgEGBSuBBAAKBG0wawIBAQQgDQKlS7bO/Kk5ki6EX2jc7fwpBZdQSfLLkydhhpfNJp+hRANCAASvzBZG6h3rpDOLy9Fx5yW3Pa6Od3CngeFK5f8uUlPHrtxLmNl0CHBserrsk/fFJanzIKpEEIisR7AOykJ2wqgr"
    # public_key = "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEr8wWRuod66Qzi8vRcecltz2ujndwp4HhSuX/LlJTx67cS5jZdAhwbHq67JP3xSWp8yCqRBCIrEewDspCdsKoKw=="
    # print(yeepay_yop_download_cert(algorithm="SM2", serial_no=serial_no, auth_code=auth_code, private_key=private_key, public_key=public_key, pwd="qwertyuiop[]"))
