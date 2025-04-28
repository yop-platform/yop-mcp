# 境内收单-下单

## 基本信息

- **API ID**: 8c619eb57da847ae87f7bf7c453b0260
- **API 分组**: kj
- **请求路径**: `/rest/v1.0/kj/onlinepay/order`
- **请求方法**: POST
- **类型**: 
- **安全需求**: YOP-RSA2048-SHA256, YOP-SM2-SM3
- **描述**: 
- **最后更新时间**: 2022-07-13 14:45:28

## 请求参数

### application/json

| 参数名 | 参数说明 | 类型 | 是否必填 | 描述 |
| ------ | ------ | ------ | ------ | ------ |
| productDetails |  | array | 否 |  |
| &nbsp;&nbsp;└─ name |  | string | 否 | 商品名称 |
| &nbsp;&nbsp;└─ quantity |  | integer | 否 | 商品数量 |
| &nbsp;&nbsp;└─ amount | 商品金额 | integer | 否 | 为总金额，不为单价 |
| &nbsp;&nbsp;└─ receiver |  | string | 否 | 收款人名称（如果为空的话自动取注册名称） |
| &nbsp;&nbsp;└─ description |  | string | 否 | 商品描述 |
| &nbsp;&nbsp;└─ requestId | 明细请求号 | string | 否 | 传入子订单时，必传入此信息，与子订单号一致 |
| requestId |  | string | 否 | 请求号 |
| orderAmount |  | integer | 否 | 订单金额 |
| orderCurrency | 订单币种 | string | 是 | <p>默认CNY</p> |
| notifyUrl |  | string | 否 | 通知地址 |
| callbackUrl |  | string | 否 | 回调地址 |
| remark |  | string | 否 | 备注 |
| paymentModeCode |  | string | 否 | 通过支付方式编码实现直连支付方式（需开通） 参考文档 |
| authCode | 支付宝支付授权码 | string | 否 | 此参数传在支付宝注册的授权码。 |
| cashierVersion | 收银台类型 | string | 否 | STANDARD标准版DECLARE申报版 CUSTOMS海关版 按照收银台类型值判断 DECLARE需要同时提交申报信息和贸易背景。 STANDARD不需要提交申报信息和贸易背景。 CUSTOMS同申报版相似，区别在于可不传银行卡号 |
| forUse | 贸易背景 | string | 否 | GOODSTRADE货物贸易 PLANETICKET机票 HOTELACCOMMODATION酒店 STUDYABROAD留学 |
| merchantUserId | 商户会员ID | string | 否 | 用户在商户网站的会员ID，用于联名账户支付模式 |
| bindCardId | 绑卡id | string | 否 | 易宝支付返给商户的绑卡对应信息，商户在支付请求中使用，可以不再提交用户身份信息和卡信息，通过绑卡支付完成支付 |
| payer |  | object | 否 |  |
| &nbsp;&nbsp;└─ name | 付款方名称 | string | 否 | 姓名或机构名称 若以机构名义申报，需要填写已备案的机构名称，否则请填写用户姓名（若需报关此项必填） |
| &nbsp;&nbsp;└─ idType | 证件类型 | string | 否 | 身份证IDCARD, 组织机构ORG （若需报关此项必填） |
| &nbsp;&nbsp;└─ idNum | 证件号码 | string | 否 | 目前只接受18位身份证号码或9位组织机构代码，根据证件类型匹配 （若需报关此项必填） |
| &nbsp;&nbsp;└─ bankCardNum |  | string | 否 | 银行卡号 |
| &nbsp;&nbsp;└─ phoneNum |  | string | 否 | 手机号 |
| &nbsp;&nbsp;└─ email |  | string | 否 | 邮箱 |
| receiver |  | object | 否 |  |
| &nbsp;&nbsp;└─ receiver |  | string | 否 | 收货人名称 |
| &nbsp;&nbsp;└─ phoneNum |  | string | 否 | 手机号 |
| &nbsp;&nbsp;└─ address |  | string | 否 | 地址 |
| bankCard |  | object | 否 |  |
| &nbsp;&nbsp;└─ name |  | string | 否 | 付款方名称 |
| &nbsp;&nbsp;└─ cardNo |  | string | 否 | 付款方卡号 |
| &nbsp;&nbsp;└─ cvv2 |  | string | 否 | 卡CVV2 |
| &nbsp;&nbsp;└─ idNo |  | string | 否 | 付款放身份证 |
| &nbsp;&nbsp;└─ expiryDate |  | string | 否 | 卡有效期 |
| &nbsp;&nbsp;└─ mobileNo |  | string | 否 | 手机号 |
| clientIp |  | string | 否 | 请求IP |
| timeout |  | integer | 否 | 订单超时时间 |
| subOrders |  | array | 否 |  |
| &nbsp;&nbsp;└─ requestId | 子订单请求号 | string | 否 | 与商品明细中请求号保持一致 |
| &nbsp;&nbsp;└─ orderAmount |  | integer | 否 | 子订单金额 |
| openId |  | string | 否 | 微信公众号openId<br>此参数传用户自己的微信openId，如果需要用到此参数需要提前通知我方进行配置。 |

### 请求参数示例

## 响应参数

### application/json

| 参数名 | 参数说明 | 类型 | 描述 |
| ------ | ------ | ------ | ------ |
| merchantId |  | string | 商户编码 |
| status |  | string | 状态 |
| redirectUrl |  | string | 重定向地址 |
| requestId |  | string | 订单号 |
| scanCode |  | string | 二维码 |
| appParams |  | string | 支付参数 |
| errorMessage |  | string | 错误信息 |

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
            string apiUri = "/rest/v1.0/kj/onlinepay/order";
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
        api = '/rest/v1.0/kj/onlinepay/order'
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
    var yopRequest = request.NewYopRequest("POST","/rest/v1.0/kj/onlinepay/order")
    
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
        YopRequest request = new YopRequest("/rest/v1.0/kj/onlinepay/order", "POST");
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