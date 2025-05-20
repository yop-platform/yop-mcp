# yop-mcp

快速对接YOP的MCP Server

## 简介

yop-mcp 是一个快速对接易宝支付开放平台(YOP)的 MCP Server，提供了一系列工具函数，帮助开发者更便捷地获取 YOP 平台的相关信息。

## 功能特点

该 MCP Server 提供以下工具函数：

1. **yeepay_yop_overview()** - 获取易宝支付开放平台(YOP)的平台规范、产品概览、接入流程和对接工具信息
2. **yeepay_yop_product_overview()** - 获取易宝支付开放平台(YOP)的所有产品的概览信息
3. **yeepay_yop_product_detail_and_associated_apis(product_code)** - 获取指定产品的介绍、使用说明和相关 API 接口列表
4. **yeepay_yop_api_detail(api_uri)** - 获取指定 API 接口的详细定义，包括基本信息、请求参数、响应参数、示例代码等
5. **yeepay_yop_java_sdk_user_guide()** - 获取易宝支付开放平台(YOP)的 yop-java-sdk 使用说明

## 环境安装

### 前置条件

- Python 3.13 或更高版本
- pip 或 uv 包管理工具

### 安装步骤

1. 克隆仓库到本地：
```bash
git clone http://gitlab.yeepay.com/yop/yop-mcp.git
cd yop-mcp
```

2. 使用 uv 安装依赖：
```bash
uv venv
uv pip install
```

或使用 pip 安装依赖：
```bash
python -m venv .venv
source .venv/bin/activate  # 在 Windows 上使用 .venv\Scripts\activate
pip install
```

## 使用方法

### 启动服务器

```bash
python main.py
```

### 工具函数说明

#### 1. yeepay_yop_overview()

获取易宝支付开放平台(YOP)的概览信息，包括平台规范、产品概览、接入流程和对接工具等信息。

**示例调用：**
```
yeepay_yop_overview()
```

**返回：** YOP 平台概览信息（markdown 格式）

#### 2. yeepay_yop_product_overview()

获取易宝支付开放平台(YOP)的所有产品的概览信息。

**示例调用：**
```
yeepay_yop_product_overview()
```

**返回：** YOP 平台所有产品的概览信息（markdown 格式）

#### 3. yeepay_yop_product_detail_and_associated_apis(product_code)

获取指定产品的介绍、使用说明和相关 API 接口列表。

**参数：**
- `product_code`（字符串）- 产品编码，产品的唯一标识

**示例调用：**
```
yeepay_yop_product_detail_and_associated_apis("user-scan")
```

**返回：** 指定产品的介绍、使用说明和相关 API 接口列表（markdown 格式）

#### 4. yeepay_yop_api_detail(api_uri)

获取指定 API 接口的详细定义，包含基本信息、请求参数、请求示例、响应参数、响应示例、错误码、回调、示例代码等信息。

**参数：**
- `api_uri`（字符串）- API 的 URI 路径，支持以下格式：
  - `/rest/v1.0/aggpay/pre-pay`
  - `https://open.yeepay.com/docs-v3/api/post_rest_v1.0_aggpay_pre-pay.md`
  - `https://open.yeepay.com/docs-v2/apis/user-scan/post__rest__v1.0__aggpay__pre-pay/index.html`

**示例调用：**
```
yeepay_yop_api_detail("/rest/v1.0/aggpay/pre-pay")
```

**返回：** API 接口的详细定义信息（markdown 格式）

#### 5. yeepay_yop_java_sdk_user_guide()

获取易宝支付开放平台(YOP)的 yop-java-sdk 使用说明。

**示例调用：**
```
yeepay_yop_java_sdk_user_guide()
```

**返回：** yop-java-sdk 使用说明（markdown 格式）

## 常见问题

1. **如何查找产品编码？**
   可以通过调用 `yeepay_yop_product_overview()` 获取产品概览，从中找到需要的产品编码。

2. **如何获取完整的 API 列表？**
   先通过 `yeepay_yop_product_overview()` 获取产品编码，然后调用 `yeepay_yop_product_detail_and_associated_apis(product_code)` 获取特定产品的 API 列表。

3. **接口返回错误怎么办？**
   系统已内置容错机制，如果特定接口请求失败，会尝试备用地址获取信息。

## 注意事项

- 所有接口返回的数据均为 markdown 格式，方便直接展示
- 确保网络连接正常，能够访问易宝支付开放平台

## 贡献指南

欢迎提交 Issue 或 Pull Request 来改进这个项目。

## 许可证

[LICENSE 信息]






