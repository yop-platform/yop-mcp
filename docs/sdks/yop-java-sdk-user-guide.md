# 使用Java-SDK(RSA)

## 概述

易宝开放平台官方SDK封装了请求的签名、加密、响应的验签、解密等功能，并提供了性能优化和多域名动态切换等特性，使开发者能够轻松、快速地完成API调用和结果通知处理。

易宝SDK分为两种类型：

* **基础SDK**：实现了API和结果通知的调用过程
* **业务SDK**：在基础SDK之上，增加了对API参数的打包，能更便捷地进行参数赋值

**推荐使用业务SDK**，如有特殊需求，也可以参考[SDK源码](https://github.com/yop-platform/yop-java-sdk)或[无SDK对接API](/docs/open/platform-doc/sdk_guide-sm/no-sdk-sm)自行实现。

基础SDK各版本变更记录，请前往GitHub[查看](https://github.com/yop-platform/yop-java-sdk/blob/develop/CHANGELOG.md)。

最新特性支持**多域名动态切换**，详见[多域名动态切换使用说明](https://yeepay.feishu.cn/docx/GcMbdzhCroGPVFxpqsvcDGdQnEg)。

## 环境要求

* 支持JDK 1.6及以上版本
* 注意：带有多域名切换特性的版本依赖sentinel，要求JDK 1.8及以上

## SDK使用

### 引入SDK

基础SDK和业务SDK二选一即可，**推荐业务SDK**。
如参考API文档中的示例代码，需与页面中选择的SDK类型保持一致。

#### 1. 引入业务SDK

业务SDK的核心会调用基础SDK，通过pom自动引入。

##### 1.1 下载业务SDK

从商户后台-开发者中心，勾选相关产品，[下载业务SDK](https://mp.yeepay.com/auth/signin?redirectUrl=https%3A%2F%2Fmp.yeepay.com%2Fyop-developer-center%2Fcas%3FredirectUrl%3Dhttps%253A%252F%252Fmp.yeepay.com%252Fmp-developer-center%252Findex.html%2523%252Fdev-services%252Ftools)到本地。

![](/yop-portal/attachments/access?fileId=qIBkQKvdTc)

##### 1.2 集成业务SDK

有三种方式集成业务SDK：源码方式（推荐）、使用依赖管理工具、使用依赖工具(shade方式)。

**注意：** 如果遇到依赖冲突情况，请使用依赖管理工具集成(shade方式)。

###### 1.2.1 源码方式集成（推荐）

1. 将`src/main/java`源码拷贝到项目中，可根据需要调整包名
2. 将`pom.xml`里的依赖添加到项目中
3. 参考`src/main/resources`下的`yop_sdk_config_default.json`、`yop_sdk_config_template.json`配置应用和密钥
4. 参考`src/test/java`下的单元测试进行开发、调试

###### 1.2.2 使用依赖管理工具(非shade方式)

根目录下执行命令 `mvn clean package -Dmaven.test.skip=true`，target目录下会生成yop-java-sdk-biz-${version}-assembly.zip压缩包，解压后文件说明如下：

```
+- pom.xml                         // maven 依赖管理文件
+- README.md                       // README 文档
+- yop_sdk_config_template.json    // 配置文件模板
+- yop-java-sdk-biz-${version}.jar          // 业务代码jar包
+- yop-java-sdk-biz-${version}-sources.jar  // 业务代码源码包
+- yop-java-sdk-biz-${version}-shade.jar    // 将部分支持shade的jar压缩为一个，方便引入
+- lib                             // 所有依赖的jar列表，如使用shade，仅需额外引入bcpkix-jdk15on、bcprov-jdk15on即可
```

**发布业务SDK到私有仓库**

参考[发布第三方jar包到远程仓库](https://maven.apache.org/guides/mini/guide-3rd-party-jars-remote.html)，示例命令：

```bash
mvn deploy:deploy-file -Dversion=${version} -DgroupId=com.yeepay.yop.sdk -DartifactId=yop-java-sdk-biz -Dpackaging=jar -Dfile=target/yop-java-sdk-biz-${version}.jar -Durl=<url-of-the-repository-to-deploy> -DrepositoryId=<id-to-map-on-server-section-of-settings.xml>
```

**在pom中引用业务SDK**
注意：仅需要引入该biz包，maven会自动引入其他依赖包

```xml
<dependency>
  <groupId>发布到私服的坐标-DgroupId</groupId>
  <artifactId>发布到私服的坐标-DartifactId</artifactId>
  <version>发布到私服的坐标-Dversion</version>
</dependency>
```

###### 1.2.3 使用依赖管理工具集成(shade方式)

**参考 1.2.2 本地编译打包【业务SDK】**

**发布业务SDK-shade包到私有仓库**

```bash
mvn deploy:deploy-file -Dversion=${version} -DgroupId=com.yeepay.yop.sdk -DartifactId=yop-java-sdk-biz-shade -Dpackaging=jar -Dfile=target/yop-java-sdk-biz-${version}-shade.jar -Durl=<url-of-the-repository-to-deploy> -DrepositoryId=<id-to-map-on-server-section-of-settings.xml>
```

**在pom中引用业务SDK-shade包**

```xml
<dependency>
  <groupId>发布到私服的坐标-DgroupId</groupId>
  <artifactId>发布到私服的坐标-DartifactId</artifactId>
  <version>发布到私服的坐标-Dversion</version>
  <exclusions>
    <exclusion>
      <groupId>*</groupId>
      <artifactId>*</artifactId>
    </exclusion>
  </exclusions>
</dependency>
<!--  以下两个包无法shade，需要单独引入  -->
<dependency>
  <groupId>org.bouncycastle</groupId>
  <artifactId>bcprov-jdk15on</artifactId>
  <version>1.67</version>
</dependency>
<dependency>
  <groupId>org.bouncycastle</groupId>
  <artifactId>bcpkix-jdk15on</artifactId>
  <version>1.67</version>
</dependency>
```

#### 2. 引入基础SDK

如果使用业务SDK，会自动引入基础SDK，可忽略该步骤，直接进入下一步【SDK配置】
基础SDK可以单独使用，以Maven为例：

```xml
<!-- 基础类包 -->
<dependency>
  <groupId>com.yeepay.yop.sdk</groupId>
  <artifactId>yop-java-sdk</artifactId>
  <version>4.4.15</version>
</dependency>
<!--  下方两个软算法包可以根据需要引入其一或者全部 -->
<!--  1.国际软算法(RSA) -->
<dependency>
  <groupId>com.yeepay.yop.sdk</groupId>
  <artifactId>yop-java-sdk-crypto-inter</artifactId>
  <version>4.4.15</version>
</dependency>
<!--  2.商密软算法(SM2) -->
<dependency>
  <groupId>com.yeepay.yop.sdk</groupId>
  <artifactId>yop-java-sdk-crypto-gm</artifactId>
  <version>4.4.15</version>
</dependency>
```

如果是JDK8以下，请使用：

```xml
<!--  支持jdk6的sdk版本 -->
<dependency>
  <groupId>com.yeepay.yop.sdk</groupId>
  <artifactId>yop-java-sdk</artifactId>
  <version>4.3.4-jdk6on</version>
</dependency>
<dependency>
  <groupId>com.yeepay.yop.sdk</groupId>
  <artifactId>yop-java-sdk-crypto-inter</artifactId>
  <version>4.3.4-jdk6on</version>
</dependency>
<dependency>
  <groupId>com.yeepay.yop.sdk</groupId>
  <artifactId>yop-java-sdk-crypto-gm</artifactId>
  <version>4.3.4-jdk6on</version>
</dependency>
```

### SDK配置

SDK默认从路径(相对classPath) `config/yop_sdk_config_default.json` 读取配置文件。

**单商编应用：** 可以在自己项目的config目录下放一份`yop_sdk_config_default.json`并修改文件中的app_key、isv_private_key，SDK会自动加载您的配置信息。如需定制配置文件加载路径，请参见：[1、配置文件路径](#SDK配置)。

**多商编应用：** 可以采用上述配置文件的形式，但考虑到动态新增商编的情况，可以实现自己的`YopCredentialsProvider`来从数据库或其他地方加载。请参见：[2、自定义ISV密钥的加载逻辑-可选](#2--自定义ISV密钥的加载逻辑-可选-)。

#### 1. 配置文件路径

如需修改读取路径可以在VM arguments中指定配置文件路径：

* mac/linux: `-Dyop.sdk.config.file=file:///home/app/yop_sdk_config_yours.json`
* windows: `-Dyop.sdk.config.file=file:///D:\workspace\config\yop_sdk_config_yours.json`

**常见容器修改JVM参数的方式：**

```
tomcat：
方式一：在$CATALINA_HOME/bin/目录下添加setenv.sh，在setenv.sh中添加JAVA_OPTS="$JAVA_OPTS -Dyop.sdk.config.file=file:///home/app/yop_sdk_config_yours.json"

方式二：在$CATALINA_HOME/bin/catalina.sh中直接添加JAVA_OPTS="$JAVA_OPTS -Dyop.sdk.config.file=file:///home/app/yop_sdk_config_yours.json"

jetty： 
在$jetty_home/bin/jetty.sh中添加JAVA_OPTIONS="-Dyop.sdk.config.file=file:///home/app/yop_sdk_config_yours.json"

weblogic：
修改user_projects\domains\base_domain\bin下的startWebLogic.cmd文件，添加set JAVA_OPTIONS=%JAVA_OPTIONS% -Dyop.sdk.config.file=file:///home/app/yop_sdk_config_yours.json
```

**配置文件内容**

通常情况下只需要填写`app_key`和`isv_private_key`即可，其中`isv_private_key`可以配置多个，想了解其他参数[请参考配置文件详细说明](#附录-配置文件详细说明)。

```json
{
  "app_key": "<Your appKey>;覆盖优先级：YopRequest >> YopConfig >> 配置文件",
  "isv_private_key": [
    {
      "app_key": "<Your appKey>",
      "store_type": "string",
      "cert_type": "RSA2048",
      "value": "<Your RSA2048 private key>"
    }
  ],
  // 如果有网络代理需求，添加如下配置即可
  //"proxy": {
  //  "host": "代理服务器ip",
  //  "port": 代理服务器端口
  //}
  //******此处省略其他属性，如有需要，参考配置说明添加相应配置即可
}
```

#### 2. 自定义ISV密钥的加载逻辑（可选）

默认会通过配置文件方式加载，可根据需要选择是否自实现。

**实现ISV密钥加载逻辑**

实现接口`YopCredentialsProvider`或继承现成的抽象类`YopFixedCredentialsProvider`：

```java
public class CustomFixedCredentialsProvider extends YopFixedCredentialsProvider {

    /**
     * 多个appKey时，指定一个默认的应用
     *
     * @return 默认应用
     */
    @Override
    public String getDefaultAppKey() {
        return "您的默认应用";
    }

    /**
     * 根据应用获取密钥信息
     *
     * @param appKey appKey
     * @return 密钥配置信息
     */
    @Override
    protected YopAppConfig loadAppConfig(String appKey) {
        // TODO 根据appKey去加载不同的密钥信息
        YopAppConfig yopAppConfig = new YopAppConfig();
        yopAppConfig.setAppKey(appKey);

        // RSA2048 example
        YopCertConfig certConfig = new YopCertConfig();
        certConfig.setCertType(CertTypeEnum.RSA2048);
        certConfig.setStoreType(CertStoreType.STRING);
        certConfig.setValue("xxx");

        // load into sdk config
        List<YopCertConfig> isvPrivateKeys = new ArrayList<>();
        isvPrivateKeys.add(certConfig);
        yopAppConfig.setIsvPrivateKey(isvPrivateKeys);

        return yopAppConfig;
    }
}
```

**将自定义的实现类注入SDK**

```java
// 注意，该注册代码需要在项目启动时即指定，且仅需指定一次即可
YopCredentialsProviderRegistry.registerProvider(Your DIY Provider);
```

#### 3. 自定义域名、代理等配置（可选）

默认从SDK的内置文件中读取，如果有特殊配置需求，可选择使用配置文件覆盖，或自定义provider进行覆盖。

**实现配置加载逻辑**

参考`com.yeepay.yop.sdk.base.config.provider.file.YopFileSdkConfigProvider`，自实现`com.yeepay.yop.sdk.config.provider.YopSdkConfigProvider`：

```java
import com.yeepay.yop.sdk.base.config.provider.YopFixedSdkConfigProvider;
import com.yeepay.yop.sdk.config.YopSdkConfig;
import com.yeepay.yop.sdk.config.provider.file.YopProxyConfig;

import java.util.Arrays;

/**
 * 自定义SDK配置
 */
public class CustomFixedSdkConfigProvider extends YopFixedSdkConfigProvider {

    @Override
    protected YopSdkConfig loadSdkConfig() {
        YopSdkConfig yopSdkConfig = new YopSdkConfig();

        // 示例：普通接口请求端点地址，配置多个时，遇到故障可以自动切换
        yopSdkConfig.setPreferredServerRoots(Arrays.asList("https://域名A","https://域名B"));
        // 示例：文件上传、下载类接口请求端点地址
        yopSdkConfig.setYosServerRoot("https://域名C");
        // 示例：沙箱环境请求地址
        yopSdkConfig.setSandboxServerRoot("https://域名D");
  
        // 示例：请求代理配置
        final YopProxyConfig proxyConfig = new YopProxyConfig();
        proxyConfig.setHost("xxx");
        proxyConfig.setPort(1234);
        yopSdkConfig.setProxy(proxyConfig);

        // 示例：国密证书分发配置
        YopCertStore yopCertStore = new YopCertStore();
        yopCertStore.setEnable(true);// 默认会开启本地存储，将远程拉取的证书存放本地文件
        yopCertStore.setPath("/tmp/yop/certs");//默认存放位置
        yopSdkConfig.setYopCertStore(yopCertStore);

        // 全局连接超时时间、读取超时时间等其他配置，可根据需要setXXX即可
        return yopSdkConfig;
    }

    @Override
    public void removeConfig(String key) {
        // 可以不实现
    }
}
```

**将自定义的实现类注入SDK**

```java
// 注意，该注册代码需要在项目启动时即指定，且仅需指定一次即可
YopSdkConfigProviderRegistry.registerProvider(Your DIY Provider);
```

## 对接API

**了解业务逻辑：**
请在文档中心了解业务场景和模型，明确需要对接的具体接口。

**查看API文档：**
了解API的请求地址、请求方式（POST/GET）、签名算法、请求参数、响应参数、[平台错误码](https://open.yeepay.com/docs/v2/platform/sdk_guide/error_code/index.html)、业务错误码、异步通知接口。

### 1. 业务SDK示例

```java
// 初始化client，该Client线程安全，请使用单例模式，多次请求共用
TradeClient api = TradeClientBuilder.builder().build();
OrderQueryRequest request = new OrderQueryRequest();
request.setParentMerchantNo("parentMerchantNo_example");
request.setMerchantNo("merchantNo_example");
request.setOrderId("orderId_example");
// 指定单次请求获取数据的超时时间, 单位：ms(可选，默认采用配置文件中的设置)
//request.getRequestConfig().setReadTimeout(3000);
// 指定单次请求建立连接的超时, 单位：ms(可选，默认采用配置文件中的设置)
//request.getRequestConfig().setConnectTimeout(3000);
// 涉及敏感参数时，业务sdk会自动设置需要加密的敏感字段，如果有强制不加密的需求，可在执行请求前做如下设置：
// request.getRequestConfig().setNeedEncrypt(false);
// 如果有特殊加密需求，也可以自行设置参数，
// 1. 如果是form类型请求：
// request.getRequestConfig().addEncryptParam("参数名")
// 2. 如果是json类型请求：
// request.getRequestConfig().addEncryptParams(YopConstants.TOTAL_ENCRYPT_PARAMS);
try {
    OrderQueryResponse response = api.orderQuery(request);
    YopQueryOrderResDTO result = response.getResult();
    LOGGER.info("result: {}", result);
} catch (YopClientException e) {
    LOGGER.error("error when calling, ex:", e);
}
```

### 2. 基础SDK通用请求示例

```java
// 1. 初始化client，该Client线程安全，请使用单例模式，多次请求共用-----------------------------
YopClient yopClient = YopClientBuilder.builder().build();
// 指定要请求的API地址和请求方式
YopRequest request = new YopRequest("API", "POST/GET");

// 2. 请求配置---------------------------------------------------------------------------
YopRequestConfig requestConfig = request.getRequestConfig();
// 请求appkey设置(可选)，否则取默认appKey
//requestConfig.setAppKey("your appkey");
// 指定单次请求获取数据的超时时间, 单位：ms(可选，默认采用配置文件中的设置)
//requestConfig.setReadTimeout(3000);
// 指定单次请求建立连接的超时, 单位：ms(可选，默认采用配置文件中的设置)
//requestConfig.setConnectTimeout(3000);
// 设置所有参数加密：用此方式，所有参数自动加密，不用单独设置某个参数
//request.getRequestConfig().setTotalEncrypt(true);

// 3. 参数配置---------------------------------------------------------------------------
// 注意：如果涉及敏感数据，有加密需求, 请调用addEncryptXXX的方法

// 设置form参数，如果加密，请用方法addEncryptParameter
request.addParameter("orderNo", "2020112412341123");

// 设置文件参数
// 示例：本地文件参数传递，如果加密，请用方法addEncryptMutiPartFile
request.addMutiPartFile("merQual", new File("/Users/xxx/SiteMesh Flow Diagram.png"));
// 示例：本地文件流参数传递，如果加密，请用方法addEncryptMultiPartFile
request.addMultiPartFile("merQual", new FileInputStream(new File("/Users/xxx/SiteMesh Flow Diagram.png")));
// 示例：远程文件参数传递，如果加密，请用方法addEncryptMultiPartFile
request.addMultiPartFile("merQual", new URL("https://www.yeepay.com/logo.png").openStream());

// 设置json参数，如果加密，请用方法setEncryptContent
request.setContent(JsonUtils.toJsonString(参数包装类));

// 4. 执行请求---------------------------------------------------------------------------
try {
    // 如果是：普通请求
    YopResponse response = yopClient.request(request);
  
    // 如果是：文件上传
    //YosUploadResponse uploadResponse = yopClient.upload(request);
  
    // 如果是：文件下载
    //YosDownloadResponse downloadResponse = yopClient.download(request);
    // 及时关闭文件流，避免连接泄漏
    /*try (YosDownloadInputStream result = downloadResponse.getResult()) {
        // TODO 保存文件
        // saveFile(result);
    } catch (java.io.IOException e) {
        LOGGER.error("io exception:", e);
    }*/
} catch (YopClientException e) {
    LOGGER.error("error when calling, ex:", e);
}
```

响应结果`YopResponse`中包括处理状态、业务结果、错误码、子错误码：

- 非文件下载的接口，返回的业务结果被解析为Map，可直接取值；也可以通过`response.getStringResult()`获取原始的字符串形式的业务结果
- 文件下载接口，为避免链接泄漏，请确保正确关闭文件流

### 3. 基于SDK对接加密机说明

为方便对接加密机，SDK统一定义了相关接口规范，详情参考[对接加密机](/docs/open/platform-doc/sdk_guide-sm/encryptor-support)。

## 附录：配置文件详细说明

### 配置示例

```json
{
  "preferred_server_roots": [
    "https://openapi-a.yeepay.com/yop-center",
    "https://openapi-h.yeepay.com/yop-center"
  ],
  "yos_server_root": "https://yos.yeepay.com/yop-center",
  "yop_cert_store": {
    "enable": true,
    "path": "/tmp/yop/certs"
  },
  "http_client": {
    "connect_timeout": 3000,
    "connect_request_timeout": 3000,
    "read_timeout": 30000,
    "max_conn_total": 200,
    "max_conn_per_route": 100,
    "retry_exceptions": [
      "java.net.UnknownHostException",
      "java.net.ConnectException:No route to host (connect failed)",
      "java.net.ConnectException:Connection refused (Connection refused)",
      "java.net.ConnectException:Connection refused: connect",
      "java.net.SocketTimeoutException:connect timed out"
    ],
    "max_retry_count": 3,
    "circuit_breaker": {
      "enable": true,
      "yop_exclude_exceptions": [
        "com.yeepay.yop.sdk.exception.YopClientException"
      ],
      "rules": [
        {
          "grade": 2,
          "count": 1,
          "time_window": 900,
          "stat_interval_ms": 300000
        }
      ]
    }
  }
}
```

### 配置说明

```yaml
- app_key: 应用标识(多个app时作为主app)
- yos_server_root: 文件类API请求地址。默认https://yos.yeepay.com/yop-center
- preferred_server_roots: 普通API请求地址列表，默认：https://openapi-a.yeepay.com/yop-center、https://openapi-h.yeepay.com/yop-center
- yop_cert_store: 用于控制平台证书的有效期校验规则
    - enable：是否启用，默认true
    - path: 本地存储路径，默认/tmp/yop/certs
    - valid_after_expire_period：平台证书过期后可用时间(毫秒)，默认24小时
    - refresh_before_expire_period：平台证书过期前开始刷新时间(毫秒)，默认72小时
- isv_private_key: 商户私钥列表，用于签名和加密会话密钥，使用加密机时无须该配置
    - app_key：应用标识
    - store_type:
        - string: 密钥文本
        - file_p12: p12格式的密钥文件
    - cert_type: RSA2048/SM2
    - value: 如果store_type为string，则该值为密钥文本；如果store_type为file_*，则该值为密钥文件路径
    - password: 如果store_type为p12，则需要密码  
- http_client:
    - connect_timeout: 全局连接超时，单位ms，默认3000，建议不超过10000
    - connect_request_timeout: 从连接池获取到连接的超时时间，单位ms，默认3000，建议不超过10000
    - read_timeout: 全局读取超时时间，单位ms，默认30000
    - max_conn_total: 最大连接数，默认200
    - max_conn_per_route: 每个域下的最大连接数，默认100
    - retry_exceptions: 当笔可重试异常列表，格式:"{异常类名}:{异常消息}"，具体参考示例
    - circuit_breaker：域名熔断配置
        - enable：是否开启熔断，默认true
        - yop_exclude_exceptions：非熔断异常列表，即出现该异常不计入失败笔数，格式:"{异常类名}:{异常消息}"，具体参考示例
        - rules：熔断规则列表
            - grade：熔断策略，默认2，按错误笔数熔断，其他可选项：1(按错误率熔断)
            - count：熔断阈值，默认1，即错误2笔后进入熔断
            - time_window：熔断间歇时长(单位s，该窗口期后，会进入半开，默认900)
            - stat_interval_ms：统计窗口时长(单位ms，失败数会在该窗口内汇总计算，默认300000)
- proxy:
    - host: 代理服务器IP
    - port:  代理服务器端口，默认值：-1
    - username: 代理账号
    - password: 代理密码
    - domain: 代理域
    - workstation: 代理工作站
```
