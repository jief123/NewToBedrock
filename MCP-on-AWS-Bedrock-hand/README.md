# MCP on AWS Bedrock
A simple and clear example for implementation and understanding Anthropic MCP (on AWS Bedrock).

> For multiple MCP server and more agent implmentation, you can reference [Strands Agent SDK](https://strandsagents.com/latest/) 

## Overview
This project demonstrates how to implement and use Anthropic's Model Context Protocol (MCP) with AWS Bedrock. It provides a client implementation that can interact with MCP-enabled tools through AWS Bedrock's runtime service.

## Updates 2025-06-04: InvokeModel API Support

- Added support for AWS Bedrock's `invoke_model` API with Claude models
- Created new client implementations that use the `invoke_model` API instead of `converse` API
- Added proper tool format conversion between MCP and Claude's expected format
- Implemented correct message sequencing for tool use with Claude models

### Tool Format Conversion

The project includes a `convert_tool_format` function that handles the necessary transformations between MCP's tool format and Claude's expected format:

- MCP tools use a format with `name`, `description`, and `inputSchema` properties
- Claude in Bedrock (same as Anthropic's API) expects `name`, `description`, and `input_schema` 
- The structure of the schema itself is also different - Claude expects a specific format with `type`, `properties`, and `required` fields

This conversion ensures compatibility between MCP tools and AWS Bedrock's Claude models.

## Updates 2025-05-10: Streamable HTTP

- Add support for [Streamable HTTP](https://github.com/modelcontextprotocol/python-sdk/releases/tag/v1.8.0)
- Rewrite the URL fetching MCP server `fetch_url_mcp_server.py` that demonstrates different transport types

### Usage Instructions

Run the server with default stdio settings (no transport parameter):
```bash
# client with converse API
uv run client_stdio.py

# client with invoke_model API
uv run client_stdio_invokeMethod.py
```

Run with streamable-http transport on default port (8000):
```bash
python fetch_url_mcp_server.py --transport streamable-http

# client with converse API
uv run client_streamablehttp.py

# client with invoke_model API
uv run client_streamablehttp_invoke_model.py
```

Run with streamable-http transport on custom port:
```bash
python fetch_url_mcp_server.py --transport streamable-http --port 8080
```

## Prerequisites
- Python 3.10 or higher
- AWS account with Bedrock access
- Configured AWS credentials
- UV package manager

## Features
- Seamless integration with AWS Bedrock runtime using both Converse API and InvokeModel API
- Tool format conversion for Bedrock compatibility with different model types
- Asynchronous communication handling
- Structured logging for debugging
- Support for both stdio and streamable HTTP transports

## API Differences

### Converse API
- A unified interface provided by AWS Bedrock, offering a model-agnostic API development experience
- Allows developers to interact with different models using the same format
- Uses `toolSpec` format to define tools
- Standardizes request and response formats across different models

### InvokeModel API
- Provides API encapsulation compatible with original model providers, maintaining consistency with the original model APIs
- Requires requests to be structured according to each model provider's specific format
- For Claude models, requires specific tool formats and message sequence handling
- Allows developers to directly use model-specific parameters and formats

## Contributing
Feel free to submit issues and pull requests to improve the implementation.

## License
MIT License

## References
- [Anthropic MCP](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [AWS Bedrock](https://aws.amazon.com/bedrock/)
- [Anthropic Claude API](https://docs.anthropic.com/en/api/messages)
- [AWS Bedrock Claude Tool Use](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-anthropic-claude-messages-tool-use.html)
