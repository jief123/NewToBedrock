# AWS Bedrock 上的 MCP 实现
这是一个简单明了的示例项目，用于实现和理解 AWS Bedrock 上的 Anthropic MCP（Model Context Protocol）。

> 如需管理多个 MCP 服务器或者更多的Agent样例, 可以看看这个项目 [Strands Agent SDK](https://strandsagents.com/latest/) 


## 概述
本项目展示了如何在 AWS Bedrock 上实现和使用 Anthropic 的模型上下文协议（MCP）。它提供了一个客户端实现，可以通过 AWS Bedrock 的运行时服务与支持 MCP 的工具进行交互。

## 更新 2025-06-04：支持 InvokeModel API

- 增加了对 AWS Bedrock 的 `invoke_model` API 与 Claude 模型的支持
- 创建了使用 `invoke_model` API 而非 `converse` API 的新客户端实现
- 添加了 MCP 和 Claude 预期格式之间的正确工具格式转换
- 实现了 Claude 模型工具使用的正确消息序列处理

### 工具格式转换

项目包含一个 `convert_tool_format` 函数，用于处理 MCP 工具格式和 Claude 预期格式之间的必要转换：

- MCP 工具使用带有 `name`、`description` 和 `inputSchema` 属性的格式
- Bedrock 上的 Claude（与 Anthropic API 相同）需要 `name`、`description` 和 `input_schema` 
- 模式结构本身也不同 - Claude 需要带有 `type`、`properties` 和 `required` 字段的特定格式

这种转换确保了 MCP 工具与 AWS Bedrock 的 Claude 模型之间的兼容性。

## 更新 2025-05-10：支持 Streamable HTTP

- 增加对 [Streamable HTTP](https://github.com/modelcontextprotocol/python-sdk/releases/tag/v1.8.0) 的支持
- 重写了 URL 获取 MCP 服务器 `fetch_url_mcp_server.py`，展示了不同的传输类型

### 使用说明

使用默认 stdio 设置运行服务器（无传输参数）：
```bash
uv run fetch_url_mcp_server.py

# 使用 converse API 的客户端
uv run client_stdio.py

# 使用 invoke_model API 的客户端
uv run client_stdio_invokeMethod.py
```

使用默认端口（8000）的 streamable-http 传输运行：
```bash
python fetch_url_mcp_server.py --transport streamable-http

# 使用 converse API 的客户端
uv run client_streamablehttp.py

# 使用 invoke_model API 的客户端
uv run client_streamablehttp_invoke_model.py
```

使用自定义端口的 streamable-http 传输运行：
```bash
python fetch_url_mcp_server.py --transport streamable-http --port 8080
```

## 前提条件
- Python 3.10 或更高版本
- 具有 Bedrock 访问权限的 AWS 账户
- 已配置的 AWS 凭证
- UV 包管理器

## 功能特点
- 与 AWS Bedrock 运行时无缝集成，同时支持 Converse API 和 InvokeModel API
- 为不同模型类型提供 Bedrock 兼容的工具格式转换
- 异步通信处理
- 结构化日志记录，便于调试
- 支持 stdio 和 streamable HTTP 传输

## API 差异

## API 差异

### Converse API
- AWS Bedrock 提供的统一接口，提供与模型无关的 API 开发体验
- 让开发者可以使用相同的格式与不同的模型交互
- 使用 `toolSpec` 格式定义工具
- 标准化了不同模型的请求和响应格式

### InvokeModel API
- 提供与原始模型厂商兼容的 API 封装，保持与原始模型 API 的一致性
- 需要按照每个模型提供商的特定格式构造请求
- 对于 Claude 模型，需要特定的工具格式和消息序列处理
- 允许开发者直接使用模型特定参数和格式

## 贡献
欢迎提交问题和拉取请求以改进实现。

## 许可证
MIT 许可证

## 参考资料
- [Anthropic MCP](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [AWS Bedrock](https://aws.amazon.com/bedrock/)
- [Anthropic Claude API](https://docs.anthropic.com/en/api/messages)
- [AWS Bedrock Claude 工具使用](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-anthropic-claude-messages-tool-use.html)
