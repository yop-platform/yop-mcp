# 查询整改协查结果

## 基本信息

- **API ID**: 759122d490e3478b95488781b9d48421
- **API 分组**: mer
- **请求路径**: `/rest/v1.0/mer/rectification/result/query`
- **请求方法**: POST
- **类型**: 
- **安全需求**: YOP-RSA2048-SHA256, YOP-SM2-SM3
- **描述**: 

- **最后更新时间**: 2025-04-17 14:14:20

## 请求参数

### application/json

| 参数名 | 参数说明 | 类型 | 是否必填 | 描述 |
| ------ | ------ | ------ | ------ | ------ |
| requestNo | 请求号 | string | 否 | <p>整改协查通知的请求号。</p> |
| merchantNo | 商户编号 | string | 否 | <p>传入需要查询整改协查结果的商户编号。</p> |

### 请求参数示例

## 响应参数

### application/json

| 参数名 | 参数说明 | 类型 | 描述 |
| ------ | ------ | ------ | ------ |
| rejectReason | 整改意见 | string | <div data-lark-html-role="root"><span class="text-only" data-eleid="3">商户的整改协查意见，请根据整改意见进行资料的补充和修改。</span></div> |
| supplyEndDate | 整改改协查截止时间 | string | <div data-lark-html-role="root"><br><div data-lark-html-role="root"><span class="text-only" data-eleid="3">商户的整改协查截止时间，请在截止时间前完成材料的补充。如果逾期未补充，审核会进行相应的处置措施。</span></div><br></div> |
| rectificationUrl | 整改协查链接 | string | <div data-lark-html-role="root"><span class="text-only" data-eleid="3">商户的整改协查链接。可以通过该链接，对商户需要整改的材料进行补充。</span></div> |
| qualificationList | 整改协查资质列表 | array | <p><span class="text-only" data-eleid="3">商户的整改协查资质列表，用于查询商户具体哪些资质需要进行补充和修改。</span></p> |
| &nbsp;&nbsp;└─ qualificationList[元素] | 数组元素 | string | - | 数组元素 |
| requestNo | 请求号 | string |  |
| merchantNo | 商户编号 | string |  |
| status | 整改协查状态 | string | <div data-lark-html-role="root"><span class="text-only" data-eleid="3">商户当前的整改协查状态。</span></div><br><div data-lark-html-role="root"><span class="text-only" data-eleid="5">待整改：代表商户需要进行材料的整改；</span></div><br><div data-lark-html-role="root"><span class="text-only" data-eleid="7">审核中：代表商户整改协查材料已经提交，等待审核完成；</span></div><br><div data-lark-html-role="root"><span class="text-only" data-eleid="9">审核完成：代表商户的整改协查已经完成，当前状态为业务<span class="text-only text-with-abbreviation text-with-abbreviation-bottomline">终态；</span></span></div><br><div data-lark-html-role="root"><span class="text-only" data-eleid="11">审核拒绝：代表商户的整改协查材料已经被审核拒绝，请联系运营。</span></div><br>可选项如下:<br>WAITING_SUBMIT:待整改<br>PENDING:审核中<br>COMPLETE:审核完成<br>AUDIT_TERMINATED:审核拒绝<br> |
| returnCode | 响应编码 | string |  |
| returnMsg | 响应描述 | string |  |

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
            string apiUri = "/rest/v1.0/mer/rectification/result/query";
            /*测试私钥*/
            string private_key = "MIIEpAIBAAKCAQEAhWf5Bkq9+JsHDQkqEV8be+0Zm6AjU/6w7dw8c7iDDh3F1Q9cJkSb3MBrxD0HFQSF/Lh65Yj8U041hYi4mDs9sYLfoIZEVpXgOXd2OLsPJR/pFl32xpQddsRznMyyEsoQPPBg782dgP3Ly0QWJmfulpOzDSA6DTO3Q+aeySMiYs/VR1pr0Z4yrSvZCTyP+xFH8zys2uUxIG/LsUSsaivy9M/0WyNMG7caWc6oblWMqdcbk9wv0Ry0BRxIUGzl63tYNUf8Z1TqDpFAsG4C4+JZGSRNDCnFVAh4GcnJsRqpyDwqnaB1mbF9W+8Zoh4sOLmR+V0HjzIrB3AzS9wvIlCHFQIDAQABAoIBABPo+ZSD0ShqUroSVRH0pNBxCXJdiwg9KcDGLsuCjSStMtpiiXk4oh5nJW5LQWRUoX6fNdBOCoKQWJKOXiZyKPn2M1Ps1gQqKCXLe3xqBo+e3JW2/l6SuncASNTtA+Kj/5posb74a/pVZnX2umuO9V/JuV5LIf7YahCbObWBJd+jNiUgXYpwDB5GsosjvYoE/Limc41vmrnvpTV6s9WiipJO+P6zm4xEJqPEgFJ6QjX7NkkyN4sPvbDGB5hz/97LT3H+aAWvjEwDj4Z85irOkBnEW9BWn2vM2fLoA4cmGhROZ81SSMTzX/O7wrqXDVUyQzcMa7FIzF9QXd9tyjzqwEECgYEA7XGbClhgjLt5cuZCO4UraU07FnjIxKe+d3vBEuy3bJWtKu3AvVZ0WTsQVorbilQi4zxClkoUVku5G+uXhvljn4CZunApufLucX6ZfF20oQqik4gjmDGpvJFrfT09Z5S6ENXIKZAJXmTfgg/1tnlPT/Il2XghZt0D/4j9Pa+0OdECgYEAj9Ty8149qOteJvV0in0A1bue6MDT5L/SWxAqz9fLkk9/ChVmr8CIAtfWKUtlKEDinj/6hp+F+k4O9u+CeM9okHGGL6RQzJvjarbo5bKTTK+DH3ErAh7hwxpjuzaaP88K9R6AiTLFYpgB5DJlZKZuJZ9D4X0nflve42OBLF8IhgUCgYEA7UbwyybD3P7ff62QFFCgsAsIeA1de/+w+0/FAjdhmPX95X9PcyW5AQ5f5ku+1f38Gx414F/I8O+c3MTSWIRRRKxLcx7w46xbETmVAc3WWnP5QPrzrvw6BYFAbBfNi/v48CfibX5NjnG5VQzD24RgeKCfqDE/F77XZv2rK4Cw1nECgYBU48JgkQajZAc1xzj5Y73SZ+HqTaTCJdTpmikqcprbx7+bG/Z3VJLx2qGzzaPulh0qeWhLfGt+yANdCw9ebkuwtNAV3k0x9e/LVBkxOKxnXk9th0VzAvcMR88E970iW/iDo3UJhMWq4zx6iqP9O51W5yERPOTKVz69xkS/A3fsYQKBgQC4tYGtRYaZN5RbR9BTIoeuCJKD6qDf89xeEKLpvwIe62JVlqDW3uo7cLVOqlzV59dtuMpEC+L9NdLyb+6Fs/tOuSaT1DK8na3BOYzPWgrBPdz1sjsrRcxsVNPKU9byxMJWU0YGq5ZVUPT3w1S/Bw530SxHnheKOzEQSQZ/KXt5Bg==";
            /*测试公钥*/
            string yop_public_key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA6p0XWjscY+gsyqKRhw9MeLsEmhFdBRhT2emOck/F1Omw38ZWhJxh9kDfs5HzFJMrVozgU+SJFDONxs8UB0wMILKRmqfLcfClG9MyCNuJkkfm0HFQv1hRGdOvZPXj3Bckuwa7FrEXBRYUhK7vJ40afumspthmse6bs6mZxNn/mALZ2X07uznOrrc2rk41Y2HftduxZw6T4EmtWuN2x4CZ8gwSyPAW5ZzZJLQ6tZDojBK4GZTAGhnn3bg5bBsBlw2+FLkCQBuDsJVsFPiGh/b6K/+zGTvWyUcu+LUj2MejYQELDO3i2vQXVDk7lVi2/TcUYefvIcssnzsfCfjaorxsuwIDAQAB";
            YopRequest request = new YopRequest(appKey, private_key, "https://openapi.yeepay.com/yop-center", yop_public_key);

            string jsonBody = "";
            request.setContent(jsonBody);

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

class Client(object):
    def __init__(self, client):
        self.client = client

    def (self):
        api = '/rest/v1.0/mer/rectification/result/query'
        params = {}
        res = self.client.post_json(api=api, params=params)
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


func () {
    var priKey = &request.IsvPriKey{Value: "isvPriKey", CertType: request.RSA2048}
    var yopRequest = request.NewYopRequest("POST","/rest/v1.0/mer/rectification/result/query")
    
    // 设置json请求报文
    var params = map[string]any{}
    
    yopRequest.Content = utils.ParseToJsonStr(params)
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
        YopRequest request = new YopRequest("/rest/v1.0/mer/rectification/result/query", "POST");
        String jsonContent = "";
        request.setContent(jsonContent);

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