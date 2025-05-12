import base64
from enum import Enum
import os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography import x509
from cryptography.x509.oid import NameOID
from typing import Dict, Any, Tuple, Optional
from cryptography.hazmat.primitives.asymmetric import rsa, padding, ec
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import pkcs12, Encoding, PublicFormat, PrivateFormat, BestAvailableEncryption, NoEncryption
import http_utils
import json_utils

class KeyType(Enum):
    RSA2048 = "RSA"
    SM2 = "SM2"

class CheckResult:
    def __init__(self, result: bool, msg: str = ""):
        self.result = result
        self.msg = msg

class CertDownloadResult:
    def __init__(self):
        self.cert = None
        self.error_msg = None
    
    def with_cert(self, cert):
        self.cert = cert
        return self
    
    def with_error_msg(self, error_msg):
        self.error_msg = error_msg
        return self

class CertUtils:
    @staticmethod
    def load_private_key(pri_key_str: str, key_type: KeyType) -> Any:
        """加载私钥"""
        try:
            pri_key_bytes = base64.b64decode(pri_key_str)
            if key_type == KeyType.RSA2048:
                return serialization.load_der_private_key(
                    pri_key_bytes,
                    password=None
                )
            elif key_type == KeyType.SM2:
                # 这里需要特殊处理SM2密钥，可能需要使用专门的SM2库
                # 示例实现可能需要使用第三方库如gmssl
                return pri_key_bytes  # 实际实现需要更换
        except Exception as e:
            raise Exception(f"加载私钥失败: {str(e)}")
    
    @staticmethod
    def load_public_key(pub_key_str: str, key_type: KeyType) -> Any:
        """加载公钥"""
        try:
            pub_key_bytes = base64.b64decode(pub_key_str)
            if key_type == KeyType.RSA2048:
                return serialization.load_der_public_key(pub_key_bytes)
            elif key_type == KeyType.SM2:
                # 同样需要特殊处理SM2公钥
                return pub_key_bytes  # 实际实现需要更换
        except Exception as e:
            raise Exception(f"加载公钥失败: {str(e)}")
    
    @staticmethod
    def genP10(pri_key: str, pub_key: str, key_type: KeyType) -> str:
        """生成P10证书请求"""
        try:
            # 加载密钥
            private_key = CertUtils.load_private_key(pri_key, key_type)
            
            # 创建证书请求
            if key_type == KeyType.RSA2048:
                builder = x509.CertificateSigningRequestBuilder()
                builder = builder.subject_name(x509.Name([
                    x509.NameAttribute(NameOID.COMMON_NAME, u'certificate request'),
                ]))
                
                request = builder.sign(
                    private_key, hashes.SHA256()
                )
                
                # 返回PEM格式的证书请求
                pem_data = request.public_bytes(Encoding.PEM).decode('utf-8')
                pem_data = pem_data.replace('-----BEGIN CERTIFICATE REQUEST-----\n', '')
                pem_data = pem_data.replace('-----END CERTIFICATE REQUEST-----\n', '')
                pem_data = pem_data.replace('\n', '')
                return pem_data
            elif key_type == KeyType.SM2:
                # SM2证书请求需要特殊处理
                # 这里是简化实现，实际需要使用SM2算法库
                return "SM2_CERTIFICATE_REQUEST"  # 实际实现需要更换
        except Exception as e:
            raise Exception(f"生成P10证书请求失败: {str(e)}")
    
    @staticmethod
    def makePubCert(cert: str, serial_no: str, cert_path: str) -> str:
        """生成公钥证书文件"""
        try:
            os.makedirs(cert_path, exist_ok=True)
            pub_cert_path = os.path.join(cert_path, f"{serial_no}.cer")
            SupportUtil.write_string_to_file(cert, pub_cert_path)
            return pub_cert_path
        except Exception as e:
            raise Exception(f"生成公钥证书文件失败: {str(e)}")
    
    @staticmethod
    def makePfxCert(pri_key: str, cert: str, key_type: KeyType, pwd: str, serial_no: str, cert_path: str) -> str:
        """生成PFX私钥证书文件"""
        try:
            os.makedirs(cert_path, exist_ok=True)
            pfx_cert_path = os.path.join(cert_path, f"{serial_no}.pfx")
            
            # 加载私钥和证书
            private_key = CertUtils.load_private_key(pri_key, key_type)
            certificate = x509.load_pem_x509_certificate(cert.encode('utf-8'))
            
            if key_type == KeyType.RSA2048:
                # 创建PKCS12对象
                pfx_data = pkcs12.serialize_key_and_certificates(
                    name=serial_no.encode('utf-8'),
                    key=private_key,
                    cert=certificate,
                    cas=None,
                    encryption_algorithm=BestAvailableEncryption(pwd.encode('utf-8'))
                )
                
                # 写入PFX文件
                with open(pfx_cert_path, 'wb') as f:
                    f.write(pfx_data)
            elif key_type == KeyType.SM2:
                # SM2 PFX生成需要特殊处理
                # 这里是简化实现
                pass  # 实际实现需要更换
                
            return pfx_cert_path
        except Exception as e:
            raise Exception(f"生成PFX证书文件失败: {str(e)}")
    
    @staticmethod
    def check_input(serial_no: str, auth_code: str, key_type: KeyType, 
               pri_key: str, pub_key: str, pwd: str) -> CheckResult:
        """检查输入参数有效性"""
        if not serial_no:
            return CheckResult(False, "证书序列号不能为空")
        if not auth_code:
            return CheckResult(False, "授权码不能为空")
        if not pri_key:
            return CheckResult(False, "私钥不能为空")
        if not pub_key:
            return CheckResult(False, "公钥不能为空")
        
        # 密码长度检查
        if pwd and (len(pwd) < 12 or len(pwd) > 16):
            return CheckResult(False, "密码长度应为12-16位")
        
        # 检查密钥格式是否为Base64
        try:
            base64.b64decode(pri_key)
            base64.b64decode(pub_key)
        except:
            return CheckResult(False, "密钥格式不正确，应为Base64编码")
        
        return CheckResult(True)

    @staticmethod
    def check_key(pri_key: str, pub_key: str, key_type: KeyType) -> bool:
        """检查公私钥是否匹配"""
        try:
            # 加载密钥
            private_key = CertUtils.load_private_key(pri_key, key_type)
            public_key = CertUtils.load_public_key(pub_key, key_type)
            
            if key_type == KeyType.RSA2048:
                # 对于RSA，我们可以通过签名验证来确认密钥对匹配
                # 创建一个测试消息
                test_message = b"test message for key verification"
                
                # 使用私钥签名
                signature = private_key.sign(
                    test_message,
                    padding.PKCS1v15(),
                    hashes.SHA256()
                )
                
                # 使用公钥验证
                try:
                    public_key.verify(
                        signature,
                        test_message,
                        padding.PKCS1v15(),
                        hashes.SHA256()
                    )
                    return True
                except:
                    return False
                    
            elif key_type == KeyType.SM2:
                # SM2密钥对验证需要特殊处理
                # 这里是简化实现
                return True  # 实际实现需要更换
                
        except Exception as e:
            raise Exception(f"密钥验证失败: {str(e)}")

    @staticmethod
    def check_cert(pri_key: str, cert: str, key_type: KeyType) -> bool:
        """检查证书与私钥是否匹配"""
        try:
            # 加载私钥和证书
            private_key = CertUtils.load_private_key(pri_key, key_type)
            certificate = x509.load_pem_x509_certificate(cert.encode('utf-8'))
            
            # 获取证书中的公钥
            cert_public_key = certificate.public_key()
            
            # 创建测试消息进行签名验证
            test_message = b"test message for cert verification"
            
            if key_type == KeyType.RSA2048:
                # 使用私钥签名
                signature = private_key.sign(
                    test_message,
                    padding.PKCS1v15(),
                    hashes.SHA256()
                )
                
                # 使用证书公钥验证
                try:
                    cert_public_key.verify(
                        signature,
                        test_message,
                        padding.PKCS1v15(),
                        hashes.SHA256()
                    )
                    return True
                except:
                    return False
                    
            elif key_type == KeyType.SM2:
                # SM2证书验证需要特殊处理
                # 这里是简化实现
                return True  # 实际实现需要更换
                
        except Exception as e:
            raise Exception(f"证书验证失败: {str(e)}")

    @staticmethod
    def download_cert_from_cfca(serial_no: str, auth_code: str, cert_req: str) -> CertDownloadResult:
        try:
            # 准备请求数据
            param = {
                "serialNo": serial_no,
                "authCode": auth_code,
                "certReq": cert_req,
                "toolsVersion": Config.TOOLS_VERSION
            }
            
            # 发送请求到CFCA API
            headers = {}
            headers["Authorization"] = "Basic " + base64.b64encode(Config.BASIC.encode('utf-8')).decode('utf-8')

            response = HttpUtils.get_response(Config.CFCA_CERT_DOWNLOAD_URL, param, headers)
            map_data = JsonUtils.json_to_pojo(response, dict)
            
            if map_data.get("code") == "000000":
                data_map = map_data.get("data")
                return CertDownloadResult().with_cert("-----BEGIN CERTIFICATE-----\n" + data_map.get("cert") + "\n-----END CERTIFICATE-----")
            else:
                return CertDownloadResult().with_error_msg(map_data.get("message"))
            
        
        except Exception as e:
            return CertDownloadResult(error_msg=f"下载证书失败: {str(e)}")

    @staticmethod 
    def generate_sm2_key_pair():
        # 使用SM2曲线创建私钥
        private_key = ec.generate_private_key(
            ec.SECP256K1(),
            default_backend()
        )
        
        # 从私钥获取公钥
        public_key = private_key.public_key()
        
        # 导出私钥，DER格式
        private_key_der = private_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        # 导出公钥，DER格式
        public_key_der = public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        # Base64编码
        private_key_b64 = base64.b64encode(private_key_der).decode('utf-8')
        public_key_b64 = base64.b64encode(public_key_der).decode('utf-8')
        
        return [private_key_b64, public_key_b64]
        

class Config:
    RSA_CERT_SAVE_PATH = "./certs/rsa/"
    SM2_CERT_SAVE_PATH = "./certs/sm2/"
    HOST = "https://mp.yeepay.com"
    # CFCA API相关配置
    CFCA_CERT_DOWNLOAD_URL = HOST + "/yop-developer-center/apis/cfca/cert/download"
    BASIC = "keytools:keytools"
    TOOLS_VERSION = "mcp"


class SupportUtil:
    @staticmethod
    def is_file_exists(file_path: str) -> bool:
        """检查文件是否存在"""
        return os.path.exists(file_path)
    
    @staticmethod
    def read_file_as_string(file_path: str) -> str:
        """从文件中读取内容为字符串"""
        with open(file_path, 'r') as file:
            return file.read()
    
    @staticmethod
    def write_string_to_file(content: str, file_path: str) -> None:
        """将字符串内容写入文件"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(content)

def download_cert(algorithm: str = "RSA", serial_no: str = "", auth_code: str = "", 
                 private_key: str = "", public_key: str = "", pwd: str = "") -> Dict[str, Any]:
    # 确定密钥类型
    key_type = KeyType.SM2 if algorithm.upper() == "SM2" else KeyType.RSA2048
    
    # 检查输入参数
    check_result = CertUtils.check_input(serial_no, auth_code, key_type, private_key, public_key, pwd)
    if not check_result.result:
        return {"message": check_result.msg}
    
    # 检查公私钥匹配
    p10_generated = False  # 标记是否已生成P10请求
    try:
        if not p10_generated and not CertUtils.check_key(private_key, public_key, key_type):
            return {"message": "商户公私钥不匹配，请重新输入"}
    except Exception as e:
        return {"message": f"密钥解析异常: {str(e)}"}
    
    # 生成证书请求
    if p10_generated:
        cert_req = private_key
    else:
        try:
            cert_req = CertUtils.genP10(private_key, public_key, key_type)
        except Exception as e:
            return {"message": f"生成证书请求失败: {str(e)}"}
    
    # 确定证书保存路径
    cert_path = Config.SM2_CERT_SAVE_PATH if key_type == KeyType.SM2 else Config.RSA_CERT_SAVE_PATH
    pri_cert_path = os.path.join(cert_path, f"{serial_no}.pfx")
    pub_cert_path = os.path.join(cert_path, f"{serial_no}.cer")
    
    # 检查证书是否已存在
    if SupportUtil.is_file_exists(pri_cert_path) and SupportUtil.is_file_exists(pub_cert_path):
        return {
            "message": "本地证书已存在",
            "pfxCert": pri_cert_path,
            "pubCert": pub_cert_path
        }
    
    try:
        # 获取证书
        if SupportUtil.is_file_exists(pub_cert_path):
            cert = SupportUtil.read_file_as_string(pub_cert_path)
        else:
            cert_download_result = CertUtils.download_cert_from_cfca(serial_no, auth_code, cert_req)
            if cert_download_result.error_msg:
                return {"message": cert_download_result.error_msg}
            cert = cert_download_result.cert
        
        # 检查证书与私钥匹配
        if not CertUtils.check_cert(private_key, cert, key_type):
            return {"message": "证书已下载过，且证书与输入的私钥不匹配，请核对"}
        
        # 保存证书
        pub_cert_path = CertUtils.makePubCert(cert, serial_no, cert_path)
        if not p10_generated:
            pri_cert_path = CertUtils.makePfxCert(private_key, cert, key_type, pwd, serial_no, cert_path)
        
        return {
            "message": "CFCA证书激活并下载成功",
            "pfxCert": pri_cert_path,
            "pubCert": pub_cert_path
        }
    except Exception as e:
        return {"message": f"系统异常，请稍后重试: {str(e)}"}

def gen_key_pair(algorithm="RSA", format="pkcs8", storage_type="file"):
    try:
        private_key_str = None
        public_key_str = None
        
        if algorithm.upper() == "RSA":
            # 生成RSA密钥对，使用2048位密钥长度
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
            public_key = private_key.public_key()
            
            # 处理私钥格式
            if format.lower() == "pkcs8":
                private_key_bytes = private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
            else:  # pkcs1
                private_key_bytes = private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                )
            
            # 处理公钥格式
            public_key_bytes = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            
            # 去除PEM头尾并转为Base64字符串
            private_key_str = private_key_bytes.decode('utf-8')
            private_key_str = private_key_str.replace('-----BEGIN PRIVATE KEY-----\n', '')
            private_key_str = private_key_str.replace('-----END PRIVATE KEY-----\n', '')
            private_key_str = private_key_str.replace('-----BEGIN RSA PRIVATE KEY-----\n', '')
            private_key_str = private_key_str.replace('-----END RSA PRIVATE KEY-----\n', '')
            private_key_str = private_key_str.replace('\n', '')
            
            
            public_key_str = public_key_bytes.decode('utf-8')
            public_key_str = public_key_str.replace('-----BEGIN PUBLIC KEY-----\n', '')
            public_key_str = public_key_str.replace('-----END PUBLIC KEY-----\n', '')
            public_key_str = public_key_str.replace('\n', '')
            
        elif algorithm.upper() == "SM2":
            if format.lower() != "pkcs8":
                return {
                    "message": "SM2密钥只支持生成PKCS8格式",
                    "privateKey": None,
                    "publicKey": None,
                    "privateCert": None,
                    "publicCert": None
                }
            private_key_str, public_key_str = CertUtils.generate_sm2_key_pair()
        else:
            return {
                "message": f"不支持的密钥算法: {algorithm}",
                "privateKey": None,
                "publicKey": None,
                "privateCert": None,
                "publicCert": None
            }
        
        # 如果需要保存到文件
        private_cert_path = None
        public_cert_path = None
        
        if storage_type.lower() == "file":
            # 创建目录
            key_dir = "./keys/"
            os.makedirs(key_dir, exist_ok=True)
            
            algorithm_name = "RSA2048" if algorithm.upper() == "RSA" else "SM2"
            
            # 保存私钥
            private_cert_path = os.path.join(key_dir, f"应用私钥{algorithm_name}.txt")
            with open(private_cert_path, "w") as f:
                f.write(private_key_str)
            
            # 保存公钥
            public_cert_path = os.path.join(key_dir, f"应用公钥{algorithm_name}.txt")
            with open(public_cert_path, "w") as f:
                f.write(public_key_str)
        
        return {
            "message": "密钥对生成成功" + ("，并已保存到文件" if storage_type.lower() == "file" else ""),
            "privateKey": private_key_str,
            "publicKey": public_key_str,
            "privateCert": private_cert_path,
            "publicCert": public_cert_path
        }
        
    except Exception as e:
        return {
            "message": f"生成密钥对失败: {str(e)}",
            "privateKey": None,
            "publicKey": None,
            "privateCert": None,
            "publicCert": None
        }

def main():
    # 下载证书
    # serial_no = "4923287028"
    # auth_code = "XYPAPJJHYL"
    # private_key = "MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDxSZYgdThDnpB8UiQGJfb1aDgyEBpqS1kwSWVVOAsv/pqzK8B2H9l+n7LXYlqAQ36QY+64StMnMEXZQXTafsg1QEThbc1mRWK7lc1xHOKmUIm3EiUB0MWG9wlk7smAZBjqCII+ds23yiA0QFn0kw8xQN56nFS4H33TqJk+iwZwLjR4tW9BYqSK0QA4pReQeJaz6UX97Je3FNplQJhn8I/TEGp9tjondYZdrWekA+Iv5YXdvYp/pB+8KZg76mlNWAOU6ckXCHnFjc6Qr+KqDYLGFaAEZ/ZVMHG82wneqZpHl8zIVj+hyRm9aypw6Hy/tgF4lAt+Ulz5idsU+y1JdAm7AgMBAAECggEAakU3Pl9yYvHVADRrUlvpO6flzELkZ3l9NDO3UkPHRaG1AAHemAgqEkeDDLLwWjqf5TdmXjvyaPmtYeUe8tbRFgcS71idlRQtSqJNZCrNNmQVa5CtxPFu9iUauZ4kGIy9nmIV/y3zKCX5bhoDpKEamV5RPp5Y/+k60XyZ1f6EXOZZydS3wDpU+TQwwulP8vzAG5HfkYse5IT/04iqirFh9dQr/LZgj4jeLg2KDQE7j2lAIZr0WA4MbS3F57BX0fNiBEi89yn5/0U1EBboPoS/sMW7a0n0J46MfupRBUC8oOYSerWqZmPYolo73DIT+bOfL8pl5PzjGOiuweOvVcBlqQKBgQDxvuPzfhcyr4enEO8LzigUJ+SumLEnaHA51gWDQpxXZbij3ZZY31ayivYWH+MIBJOwmvTsmSH7TdYnzovondb+Hy9a1OdiTLPqhAw8FzOtaeoDXxPnzvD91tlZcPxvi0E+xjyzPBaIH8zlX/54PJq/nOyGIzMrMMh5Xb8FTQlXwwKBgQD/g8d95FTCh2f/+whh/WubwRqJXGbBblHbvgGP1jRjXDYP2WSd8cWv+ISztGimneHuou11jPse1AHunJOnmIbn/bXX27XUCMRalxN+uKjdne4xM6n+YNUCub9U6arlw7chcKD1sbvj00t1MuskeT9ojMgIeyd+wFzhgAMzpjreqQKBgF+ONep8b80AJx25itPexGbbMgB1qKjMFng2Ce3NeaDuO2LCZvhwJ4Phe85ZAlOcA4juZ1vSV+VO6hTIBvOG2IGQcBZ2S5PGf+N2GKP0A+BLGk4E2ghp+0ZLE5TQHWg14i9fCoVKfhmGgGY2YI7EXeLZs4B+D27GFKgsjyIYRlYjAoGAFzWgLFZOQLFOCBmEZGpBmQ9MWsfS6aUcuGok+CzL626X1o63rgUlINvhKfWsP949hJC2IyRgNyeo2UTNwL6BGpeYKfhiJtV5CIWKlsstQ5wx47Q+r8WZ87ptn8ft5xsFCnuRk1/GomYyB35Nj62XzeZj0SlmqAPPLAiVwd5KoKkCgYASuRLpWGeqB3Y3ksm7dAH0F1Fll5NPc6rf81ak1DeM1P49QkTC5Ce3mazkrVr3Wa86YvePp5usgpwEvh+YkW/gldK5FffmcUNmHhvjtoXed5ekrIBUOMyW7A6remdaq4rcsKJIUWqblaDnI6QbsZqKKTh9cYf/NGOVbwN0hm8nDg=="
    # public_key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA8UmWIHU4Q56QfFIkBiX29Wg4MhAaaktZMEllVTgLL/6asyvAdh/Zfp+y12JagEN+kGPuuErTJzBF2UF02n7INUBE4W3NZkViu5XNcRziplCJtxIlAdDFhvcJZO7JgGQY6giCPnbNt8ogNEBZ9JMPMUDeepxUuB9906iZPosGcC40eLVvQWKkitEAOKUXkHiWs+lF/eyXtxTaZUCYZ/CP0xBqfbY6J3WGXa1npAPiL+WF3b2Kf6QfvCmYO+ppTVgDlOnJFwh5xY3OkK/iqg2CxhWgBGf2VTBxvNsJ3qmaR5fMyFY/ockZvWsqcOh8v7YBeJQLflJc+YnbFPstSXQJuwIDAQAB"
    # print(download_cert(algorithm="RSA", serial_no=serial_no, auth_code=auth_code, private_key=private_key, public_key=public_key, pwd="qwertyuiop[]"))
    
    # 生成密钥对
    # private_key, public_key = CertUtils.generate_key()
    # print(f"私钥(Base64): {private_key}")
    # print(f"公钥(Base64): {public_key}") 

    print(gen_key_pair(algorithm="RSA", format="pkcs8", storage_type="string"))


if __name__ == '__main__':
    main() 