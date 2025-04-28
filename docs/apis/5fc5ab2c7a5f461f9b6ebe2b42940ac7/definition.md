# 商户信息变更

## 基本信息

- **API ID**: 5fc5ab2c7a5f461f9b6ebe2b42940ac7
- **API 分组**: mer
- **请求路径**: `/rest/v1.0/mer/merchant/info/modify`
- **请求方法**: POST
- **类型**: WEB
- **安全需求**: YOP-RSA2048-SHA256, YOP-SM2-SM3
- **描述**: 商户信息变更
- **最后更新时间**: 2025-04-22 13:26:30

## 请求参数

### application/x-www-form-urlencoded

| 参数名 | 参数说明 | 类型 | 是否必填 | 描述 |
| ------ | ------ | ------ | ------ | ------ |
| requestNo | 请求号 | string | 是 |  |
| merchantNo | 商户编号 | string | 是 |  |
| notifyUrl | 回调地址 | string | 是 | 1、用于接收审核已驳回状态下的原因；<br>2、用于接收变更完成的通知。<br><br>请参考 <a href="#anchor7">变更结果通知</a> |
| merchantSubjectInfo | 商户主体信息 | string | 否 | 请参考:<a href="https://open.yeepay.com/docs/products/ptssfk/others/5f3cef4420289f001ba82523/6279e4c355c271003fd81123">商户主体信息</a> |
| merchantCorporationInfo | 法人信息 | string | 否 | 请参考:<a href="https://open.yeepay.com/docs/products/ptssfk/others/5f3cef4420289f001ba82523/627a0d58d42367003e209dc7">变更法人信息json说明</a> |
| merchantContactInfo | 商户联系人信息 | string | 否 | 请参考:<a href="https://open.yeepay.com/docs/products/ptssfk/others/5f3cef4420289f001ba82523/627a0dc34fb56f003e54b45a">商户联系人信息json说明</a> |
| industryCategoryInfo | 行业分类 | string | 否 | 请参考：<a href="https://open.yeepay.com/docs/v2/products/ptssfk/others/5f3cef4420289f001ba82523/5f3cf1c330b67d001bd7b21d/index.html">行业分类</a ></a> |
| businessAddressInfo | 经营地址信息 | string | 否 | 请参考:<a href="https://open.yeepay.com/docs/products/ptssfk/others/5f3cef4420289f001ba82523/627a10a855c271003fd81125">变更经营地址信息json说明</a> |
| accountInfo | 银行账户信息 | string | 否 | 请参考:<a href="https://open.yeepay.com/docs/products/ptssfk/others/5f3cef4420289f001ba82523/627a10bcd42367003e209dc8">变更银行账户信息json说明</a> |
| bankToken | 账户通口令信息 | string | 否 | 账户通口令信息<br>此字段只涉及与廊坊银行合作的商户，修改廊坊银行信息时需上传 |
| qualificationInfo | 资质信息 | string | 否 | 请参考:<a href="https://open.yeepay.com/docs/products/fwssfk/others/5f59fc1720289f001ba82528/67dbfe1da9a59b000119fb72">资质信息json说明</a> |
| merchantReportConfig | 商户报备配置信息 | string | 否 | 请参考:<a href="https://open.yeepay.com/docs/products/fwssfk/others/5f59fc1720289f001ba82528/6807074d269f1a000126a83f">商户报备配置信息json说明</a> |

### 请求参数示例

#### merchantSubjectInfo（商户主体信息）
```json
{
  "licenceUrl": "商户证件照片地址",
  "signName": "商户签约名",
  "licenceNo": "商户证件号码",
  "shortName": "商户简称"
}
```

#### merchantCorporationInfo（法人信息）
```json
{
  "legalName": "法人名称",
  "legalLicenceType": "ID_CARD",
  "legalLicenceNo": "法人证件编号",
  "legalLicenceFrontUrl": "法人证件人像面照片地址",
  "legalLicenceBackUrl": "法人证件非人像面照片地址"
}
```

#### merchantContactInfo（商户联系人信息）
```json
{
  "contactName": "联系人姓名",
  "contactMobile": "联系人手机号",
  "contactEmail": "联系人邮箱",
  "contactLicenceNo": "联系人证件号码",
  "servicePhone": "客服电话"
}
```

#### industryCategoryInfo（行业分类）
```json
{
  "primaryIndustryCategory": "一级行业分类编码",
  "secondaryIndustryCategory": "二级行业分类编码"
}
```

#### businessAddressInfo（经营地址信息）
```json
{
  "province": "经营省",
  "city": "经营市",
  "district": "经营区",
  "address": "经营地址"
}
```

#### accountInfo（银行账户信息）
```json
{
  "bankAccountName": "开户名称",
  "bankAccountType": "银行账户类型",
  "bankCardNo": "银行账户号码",
  "bankCardTag": "[\"SETTLEMENT\",\"WITHDRAW\"]",
  "authorizationUrl": "https://staticres.yeepay.com/xxx.文件后缀",
  "bankCode": "开户总行编码",
  "defaultSettleCard": false
}
```

#### bankToken（账户通口令信息）
```json
{
  "deviceIp": "交易ip",
  "token": "交易口令"
}
```

#### qualificationInfo（资质信息）
```json
{
  "businessPlacePhotoUrl": "https://staticres.yeepay.com/xxx.文件后缀",
  "scenePhotoUrl": "https://staticres.yeepay.com/xxx.文件后缀"
}
```

#### merchantReportConfig（商户报备配置信息）
```json
{
  "modifyReport": true,
  "reportChannels": [
    "WECHAT",
    "ALIPAY"
  ]
}
```

## 响应参数

### application/json

| 参数名 | 参数说明 | 类型 | 描述 |
| ------ | ------ | ------ | ------ |
| returnCode | 响应编码 | string |  |
| returnMsg | 响应描述 | string |  |
| applicationNo | 工单号 | string | 请求参数必填、格式、参数合法性等校验通过后返回 |
| applicationStatus | 工单状态 | string | 请求参数必填、格式、参数合法性等校验通过后返回<br>申请状态可选项如下:<br>REVIEWING:申请审核中<br>REVIEW_BACK:申请已驳回 |
| merchantNo | 商户编号 | string | 商户编号<br>接口响应成功时返回 |

## 示例代码

### CSHARP
```csharp
using System;
using System.Diagnostics;
using SDK.yop.client;

namespace Example
{
    public class Example
    {
        public static void main()
        {
            string appKey= "sdk-develop";
            string apiUri = "/rest/v1.0/mer/merchant/info/modify";
            /*测试私钥*/
            string private_key = "MIIEpAIBAAKCAQEAhWf5Bkq9+JsHDQkqEV8be+0Zm6AjU/6w7dw8c7iDDh3F1Q9cJkSb3MBrxD0HFQSF/Lh65Yj8U041hYi4mDs9sYLfoIZEVpXgOXd2OLsPJR/pFl32xpQddsRznMyyEsoQPPBg782dgP3Ly0QWJmfulpOzDSA6DTO3Q+aeySMiYs/VR1pr0Z4yrSvZCTyP+xFH8zys2uUxIG/LsUSsaivy9M/0WyNMG7caWc6oblWMqdcbk9wv0Ry0BRxIUGzl63tYNUf8Z1TqDpFAsG4C4+JZGSRNDCnFVAh4GcnJsRqpyDwqnaB1mbF9W+8Zoh4sOLmR+V0HjzIrB3AzS9wvIlCHFQIDAQABAoIBABPo+ZSD0ShqUroSVRH0pNBxCXJdiwg9KcDGLsuCjSStMtpiiXk4oh5nJW5LQWRUoX6fNdBOCoKQWJKOXiZyKPn2M1Ps1gQqKCXLe3xqBo+e3JW2/l6SuncASNTtA+Kj/5posb74a/pVZnX2umuO9V/JuV5LIf7YahCbObWBJd+jNiUgXYpwDB5GsosjvYoE/Limc41vmrnvpTV6s9WiipJO+P6zm4xEJqPEgFJ6QjX7NkkyN4sPvbDGB5hz/97LT3H+aAWvjEwDj4Z85irOkBnEW9BWn2vM2fLoA4cmGhROZ81SSMTzX/O7wrqXDVUyQzcMa7FIzF9QXd9tyjzqwEECgYEA7XGbClhgjLt5cuZCO4UraU07FnjIxKe+d3vBEuy3bJWtKu3AvVZ0WTsQVorbilQi4zxClkoUVku5G+uXhvljn4CZunApufLucX6ZfF20oQqik4gjmDGpvJFrfT09Z5S6ENXIKZAJXmTfgg/1tnlPT/Il2XghZt0D/4j9Pa+0OdECgYEAj9Ty8149qOteJvV0in0A1bue6MDT5L/SWxAqz9fLkk9/ChVmr8CIAtfWKUtlKEDinj/6hp+F+k4O9u+CeM9okHGGL6RQzJvjarbo5bKTTK+DH3ErAh7hwxpjuzaaP88K9R6AiTLFYpgB5DJlZKZuJZ9D4X0nflve42OBLF8IhgUCgYEA7UbwyybD3P7ff62QFFCgsAsIeA1de/+w+0/FAjdhmPX95X9PcyW5AQ5f5ku+1f38Gx414F/I8O+c3MTSWIRRRKxLcx7w46xbETmVAc3WWnP5QPrzrvw6BYFAbBfNi/v48CfibX5NjnG5VQzD24RgeKCfqDE/F77XZv2rK4Cw1nECgYBU48JgkQajZAc1xzj5Y73SZ+HqTaTCJdTpmikqcprbx7+bG/Z3VJLx2qGzzaPulh0qeWhLfGt+yANdCw9ebkuwtNAV3k0x9e/LVBkxOKxnXk9th0VzAvcMR88E970iW/iDo3UJhMWq4zx6iqP9O51W5yERPOTKVz69xkS/A3fsYQKBgQC4tYGtRYaZN5RbR9BTIoeuCJKD6qDf89xeEKLpvwIe62JVlqDW3uo7cLVOqlzV59dtuMpEC+L9NdLyb+6Fs/tOuSaT1DK8na3BOYzPWgrBPdz1sjsrRcxsVNPKU9byxMJWU0YGq5ZVUPT3w1S/Bw530SxHnheKOzEQSQZ/KXt5Bg==";
            /*测试公钥*/
            string yop_public_key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA6p0XWjscY+gsyqKRhw9MeLsEmhFdBRhT2emOck/F1Omw38ZWhJxh9kDfs5HzFJMrVozgU+SJFDONxs8UB0wMILKRmqfLcfClG9MyCNuJkkfm0HFQv1hRGdOvZPXj3Bckuwa7FrEXBRYUhK7vJ40afumspthmse6bs6mZxNn/mALZ2X07uznOrrc2rk41Y2HftduxZw6T4EmtWuN2x4CZ8gwSyPAW5ZzZJLQ6tZDojBK4GZTAGhnn3bg5bBsBlw2+FLkCQBuDsJVsFPiGh/b6K/+zGTvWyUcu+LUj2MejYQELDO3i2vQXVDk7lVi2/TcUYefvIcssnzsfCfjaorxsuwIDAQAB";
            YopRequest request = new YopRequest(appKey, private_key, "https://openapi.yeepay.com/yop-center", yop_public_key);
            request.addParam("requestNo", "a04cf8bded8b4413a43ab455b21eedcd");//必填
            request.addParam("merchantNo", "merchantNo_example");//必填
            request.addParam("notifyUrl", "notifyUrl_example");//必填
            request.addParam("merchantSubjectInfo", "{ \"licenceUrl\":\"商户证件照片地址\", \"signName\":\"商户签约名\", \"licenceNo\":\"商户证件号码\", \"shortName\":\"商户简称\" }");//非必填
            request.addParam("merchantCorporationInfo", "{ \"legalName\":\"法人名称\", \"legalLicenceType\":\"ID_CARD\", \"legalLicenceNo\":\"法人证件编号\", \"legalLicenceFrontUrl\":\"法人证件人像面照片地址\", \"legalLicenceBackUrl\":\"法人证件非人像面照片地址\" }");//非必填
            request.addParam("merchantContactInfo", "{ \"contactName\":\"联系人姓名\", \"contactMobile\":\"联系人手机号\", \"contactEmail\":\"联系人邮箱\", \"contactLicenceNo\":\"联系人证件号码\" ,\"servicePhone\":\"客服电话\"}");//非必填
            request.addParam("industryCategoryInfo", "{ \"primaryIndustryCategory\":\"一级行业分类编码\", \"secondaryIndustryCategory\":\"二级行业分类编码\" }");//非必填
            request.addParam("businessAddressInfo", "{ \"province\":\"经营省\", \"city\":\"经营市\", \"district\":\"经营区\", \"address\":\"经营地址\" }");//非必填
            request.addParam("accountInfo", "{\"bankAccountName\":\"开户名称\",\"bankAccountType\":\"银行账户类型\",\"bankCardNo\":\"银行账户号码\",\"bankCardTag\":\"[\\\"SETTLEMENT\\\",\\\"WITHDRAW\\\"]\",\"authorizationUrl\":\"https://staticres.yeepay.com/xxx.文件后缀\",\"bankCode\":\"开户总行编码\",\"defaultSettleCard\":false}");//非必填
            request.addParam("bankToken", "{ \"deviceIp\":\"交易ip\", \"token\":\"交易口令\"}");//非必填
            request.addParam("qualificationInfo", "{\"businessPlacePhotoUrl\":\"https://staticres.yeepay.com/xxx.文件后缀\", \"scenePhotoUrl\":\"https://staticres.yeepay.com/xxx.文件后缀\"}");//非必填
            request.addParam("merchantReportConfig", "{\"modifyReport\":true,\"reportChannels\": [\"WECHAT\",\"ALIPAY\"]}");//非必填


            try
            {
                YopResponse response = YopRsaClient.post(apiUri, request);
                if (response.isSuccess()) {
                    Debug.Print(response.stringResult);
                }
            }
            catch (Exception e)
            {
                Debug.Print("调用失败:" + e.Message );
            }
        }
    }

}
```

### PYTHON
```python
# -*- coding: utf-8 -*-

from client.yopclient import YopClient
from client.yop_client_config import YopClientConfig

# 加载默认配置文件 config/yop_sdk_config_rsa_prod.json
client = YopClient()

# 也可以加载定制配置文件
# config_file = 'config/yop_sdk_config_{}.json'.format(xxx)
# clientConfig = YopClientConfig(config_file)
# client = YopClient(clientConfig, env, cert_type)

class MerClient(object):
    def __init__(self, client):
        self.client = client

    def merchant_info_modify(self):
        api = '/rest/v1.0/mer/merchant/info/modify'
        params = {
            'requestNo': 'a04cf8bded8b4413a43ab455b21eedcd', # 必填
            'merchantNo': 'merchantNo_example', # 必填
            'notifyUrl': 'notifyUrl_example', # 必填
            'merchantSubjectInfo': '{ \"licenceUrl\":\"商户证件照片地址\", \"signName\":\"商户签约名\", \"licenceNo\":\"商户证件号码\", \"shortName\":\"商户简称\" }',
            'merchantCorporationInfo': '{ \"legalName\":\"法人名称\", \"legalLicenceType\":\"ID_CARD\", \"legalLicenceNo\":\"法人证件编号\", \"legalLicenceFrontUrl\":\"法人证件人像面照片地址\", \"legalLicenceBackUrl\":\"法人证件非人像面照片地址\" }',
            'merchantContactInfo': '{ \"contactName\":\"联系人姓名\", \"contactMobile\":\"联系人手机号\", \"contactEmail\":\"联系人邮箱\", \"contactLicenceNo\":\"联系人证件号码\" ,\"servicePhone\":\"客服电话\"}',
            'industryCategoryInfo': '{ \"primaryIndustryCategory\":\"一级行业分类编码\", \"secondaryIndustryCategory\":\"二级行业分类编码\" }',
            'businessAddressInfo': '{ \"province\":\"经营省\", \"city\":\"经营市\", \"district\":\"经营区\", \"address\":\"经营地址\" }',
            'accountInfo': '{\"bankAccountName\":\"开户名称\",\"bankAccountType\":\"银行账户类型\",\"bankCardNo\":\"银行账户号码\",\"bankCardTag\":\"[\\\"SETTLEMENT\\\",\\\"WITHDRAW\\\"]\",\"authorizationUrl\":\"https://staticres.yeepay.com/xxx.文件后缀\",\"bankCode\":\"开户总行编码\",\"defaultSettleCard\":false}',
            'bankToken': '{ \"deviceIp\":\"交易ip\", \"token\":\"交易口令\"}',
            'qualificationInfo': '{\"businessPlacePhotoUrl\":\"https://staticres.yeepay.com/xxx.文件后缀\", \"scenePhotoUrl\":\"https://staticres.yeepay.com/xxx.文件后缀\"}',
            'merchantReportConfig': '{\"modifyReport\":true,\"reportChannels\": [\"WECHAT\",\"ALIPAY\"]}'
        }
        res = self.client.post(api=api, params=params)
                # 如果要单独指定凭证，在调用 client 的对应方法时传递该凭证即可
        # credentials = YopCredentials(appKey='${appKey}',
        #                                     cert_type='RSA2048|SM2',
        #                                     priKey='${priKey}')
        # self.client.xxx(api=api, params=params, credentials=credentials)
```

### GO
```go
# -*- coding: utf-8 -*-
import (
    "github.com/yop-platform/yop-go-sdk/yop/client"
    "github.com/yop-platform/yop-go-sdk/yop/constants"
    "github.com/yop-platform/yop-go-sdk/yop/request"
    "github.com/yop-platform/yop-go-sdk/yop/utils"
)


func merchant_info_modify() {
    var priKey = &request.IsvPriKey{Value: "isvPriKey", CertType: request.RSA2048}
    var yopRequest = request.NewYopRequest("POST","/rest/v1.0/mer/merchant/info/modify")
    
    yopRequest.AddParam("requestNo", 'a04cf8bded8b4413a43ab455b21eedcd') // 必填
    yopRequest.AddParam("merchantNo", 'merchantNo_example') // 必填
    yopRequest.AddParam("notifyUrl", 'notifyUrl_example') // 必填
    yopRequest.AddParam("merchantSubjectInfo", '{ \"licenceUrl\":\"商户证件照片地址\", \"signName\":\"商户签约名\", \"licenceNo\":\"商户证件号码\", \"shortName\":\"商户简称\" }')
    yopRequest.AddParam("merchantCorporationInfo", '{ \"legalName\":\"法人名称\", \"legalLicenceType\":\"ID_CARD\", \"legalLicenceNo\":\"法人证件编号\", \"legalLicenceFrontUrl\":\"法人证件人像面照片地址\", \"legalLicenceBackUrl\":\"法人证件非人像面照片地址\" }')
    yopRequest.AddParam("merchantContactInfo", '{ \"contactName\":\"联系人姓名\", \"contactMobile\":\"联系人手机号\", \"contactEmail\":\"联系人邮箱\", \"contactLicenceNo\":\"联系人证件号码\" ,\"servicePhone\":\"客服电话\"}')
    yopRequest.AddParam("industryCategoryInfo", '{ \"primaryIndustryCategory\":\"一级行业分类编码\", \"secondaryIndustryCategory\":\"二级行业分类编码\" }')
    yopRequest.AddParam("businessAddressInfo", '{ \"province\":\"经营省\", \"city\":\"经营市\", \"district\":\"经营区\", \"address\":\"经营地址\" }')
    yopRequest.AddParam("accountInfo", '{\"bankAccountName\":\"开户名称\",\"bankAccountType\":\"银行账户类型\",\"bankCardNo\":\"银行账户号码\",\"bankCardTag\":\"[\\\"SETTLEMENT\\\",\\\"WITHDRAW\\\"]\",\"authorizationUrl\":\"https://staticres.yeepay.com/xxx.文件后缀\",\"bankCode\":\"开户总行编码\",\"defaultSettleCard\":false}')
    yopRequest.AddParam("bankToken", '{ \"deviceIp\":\"交易ip\", \"token\":\"交易口令\"}')
    yopRequest.AddParam("qualificationInfo", '{\"businessPlacePhotoUrl\":\"https://staticres.yeepay.com/xxx.文件后缀\", \"scenePhotoUrl\":\"https://staticres.yeepay.com/xxx.文件后缀\"}')
    yopRequest.AddParam("merchantReportConfig", '{\"modifyReport\":true,\"reportChannels\": [\"WECHAT\",\"ALIPAY\"]}')
    yopResp, err := client.DefaultClient.Request(yopRequest)
    if nil != err{
    // request failed
    }
    // yopResp.Result为请求结果
    
}
```

### JAVA
```java
package com.yeepay.yop.sdk.example;

import com.yeepay.yop.sdk.service.common.YopClient;
import com.yeepay.yop.sdk.service.common.YopClientBuilder;
import com.yeepay.yop.sdk.service.common.request.YopRequest;
import com.yeepay.yop.sdk.service.common.response.YopResponse;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Example {

    // 该Client线程安全，请使用单例模式，多次请求共用
    private static final YopClient client = YopClientBuilder.builder().build();
    private static final Logger LOGGER = LoggerFactory.getLogger(Example.class);

    public static void main(String[] args) {
        YopRequest request = new YopRequest("/rest/v1.0/mer/merchant/info/modify", "POST");
        request.addParameter("requestNo", "a04cf8bded8b4413a43ab455b21eedcd");
        request.addParameter("merchantNo", "merchantNo_example");
        request.addParameter("notifyUrl", "notifyUrl_example");
        request.addParameter("merchantSubjectInfo", "{ \"licenceUrl\":\"商户证件照片地址\", \"signName\":\"商户签约名\", \"licenceNo\":\"商户证件号码\", \"shortName\":\"商户简称\" }");
        request.addParameter("merchantCorporationInfo", "{ \"legalName\":\"法人名称\", \"legalLicenceType\":\"ID_CARD\", \"legalLicenceNo\":\"法人证件编号\", \"legalLicenceFrontUrl\":\"法人证件人像面照片地址\", \"legalLicenceBackUrl\":\"法人证件非人像面照片地址\" }");
        request.addParameter("merchantContactInfo", "{ \"contactName\":\"联系人姓名\", \"contactMobile\":\"联系人手机号\", \"contactEmail\":\"联系人邮箱\", \"contactLicenceNo\":\"联系人证件号码\" ,\"servicePhone\":\"客服电话\"}");
        request.addParameter("industryCategoryInfo", "{ \"primaryIndustryCategory\":\"一级行业分类编码\", \"secondaryIndustryCategory\":\"二级行业分类编码\" }");
        request.addParameter("businessAddressInfo", "{ \"province\":\"经营省\", \"city\":\"经营市\", \"district\":\"经营区\", \"address\":\"经营地址\" }");
        request.addParameter("accountInfo", "{\"bankAccountName\":\"开户名称\",\"bankAccountType\":\"银行账户类型\",\"bankCardNo\":\"银行账户号码\",\"bankCardTag\":\"[\\\"SETTLEMENT\\\",\\\"WITHDRAW\\\"]\",\"authorizationUrl\":\"https://staticres.yeepay.com/xxx.文件后缀\",\"bankCode\":\"开户总行编码\",\"defaultSettleCard\":false}");
        request.addParameter("bankToken", "{ \"deviceIp\":\"交易ip\", \"token\":\"交易口令\"}");
        request.addParameter("qualificationInfo", "{\"businessPlacePhotoUrl\":\"https://staticres.yeepay.com/xxx.文件后缀\", \"scenePhotoUrl\":\"https://staticres.yeepay.com/xxx.文件后缀\"}");
        request.addParameter("merchantReportConfig", "{\"modifyReport\":true,\"reportChannels\": [\"WECHAT\",\"ALIPAY\"]}");

        try {
            YopResponse response = client.request(request);
            LOGGER.info("result:{}", response.getResult());
        } catch (Exception ex) {
            LOGGER.error("Exception when calling, ex:", ex);
        }
    }

}

```

### 更多语言示例

可查看原始API定义文档获取Python、PHP、C#、Go等其他语言的实现示例。 