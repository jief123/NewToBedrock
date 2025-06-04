import asyncio
import json
import boto3
import logging
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def convert_tool_format(tools):
    """
    Converts tools into the format required for the Bedrock API.

    Args:
        tools (list): List of tool objects

    Returns:
        list: Tools in the format required by Bedrock
    """
    converted_tools = []

    for tool in tools:
        converted_tool = {
            "name": tool.name,
            "description": tool.description,
            "input_schema": {
                "type": "object",
                "properties": tool.inputSchema["properties"],
                "required": tool.inputSchema.get("required", [])
            }
        }
        converted_tools.append(converted_tool)

    return converted_tools


async def main():
    # Initialize Bedrock client
    bedrock = boto3.client("bedrock-runtime")

    async with streamablehttp_client("http://localhost:8000/mcp") as (
        read_stream,
        write_stream,
        _,
    ):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            # List available tools and convert to serializable format
            tools_result = await session.list_tools()
            tools_list = convert_tool_format(tools_result.tools)
            logger.info("Available tools: %s", tools_list)

            # Initial user message
            user_message = "Hello, can you help me fetch the website 'https://www.example.com'?"
            
            # Create the request body for invoke_model
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1024,
                "messages": [
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                "tools": tools_list
            }
            
            logger.info("Sending request to model: %s", json.dumps(request_body, indent=2))
            
            # Track if we're in a tool use flow
            tool_use_in_progress = False
            tool_use_data = None
            
            while True:
                # Call Bedrock with Claude model using invoke_model
                response = bedrock.invoke_model(
                    modelId="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
                    body=json.dumps(request_body)
                )
                
                # Parse the response
                response_body = json.loads(response["body"].read().decode("utf-8"))
                logger.info("Received response: %s", json.dumps(response_body, indent=2))
                
                # Extract the assistant's message
                content = response_body.get("content", [])
                stop_reason = response_body.get("stop_reason")
                
                # Print the model's response
                for item in content:
                    if item.get("type") == "text":
                        print("Model:", item["text"])
                
                # Check if the model is requesting to use a tool
                if stop_reason == "tool_use":
                    # Process tool use requests
                    for item in content:
                        if item.get("type") == "tool_use":
                            tool_use = item
                            tool_name = tool_use["name"]
                            tool_input = tool_use["input"]
                            tool_id = tool_use["id"]
                            
                            logger.info(
                                "Requesting tool %s. Request ID: %s",
                                tool_name,
                                tool_id
                            )
                            
                            try:
                                # Call the tool through the MCP session
                                tool_response = await session.call_tool(
                                    tool_name, tool_input
                                )
                                
                                # Store the assistant's message with tool_use
                                tool_use_in_progress = True
                                tool_use_data = {
                                    "role": "assistant",
                                    "content": content
                                }
                                
                                # Create a new request with the tool result
                                request_body = {
                                    "anthropic_version": "bedrock-2023-05-31",
                                    "max_tokens": 1024,
                                    "messages": [
                                        {
                                            "role": "user",
                                            "content": user_message
                                        },
                                        {
                                            "role": "assistant",
                                            "content": content
                                        },
                                        {
                                            "role": "user",
                                            "content": [
                                                {
                                                    "type": "tool_result",
                                                    "tool_use_id": tool_id,
                                                    "content": str(tool_response)
                                                }
                                            ]
                                        }
                                    ],
                                    "tools": tools_list
                                }
                                
                            except Exception as err:
                                logger.error("Tool call failed: %s", str(err))
                                # Store the assistant's message with tool_use
                                tool_use_in_progress = True
                                tool_use_data = {
                                    "role": "assistant",
                                    "content": content
                                }
                                
                                # Create a new request with the error tool result
                                request_body = {
                                    "anthropic_version": "bedrock-2023-05-31",
                                    "max_tokens": 1024,
                                    "messages": [
                                        {
                                            "role": "user",
                                            "content": user_message
                                        },
                                        {
                                            "role": "assistant",
                                            "content": content
                                        },
                                        {
                                            "role": "user",
                                            "content": [
                                                {
                                                    "type": "tool_result",
                                                    "tool_use_id": tool_id,
                                                    "content": f"Error: {str(err)}"
                                                }
                                            ]
                                        }
                                    ],
                                    "tools": tools_list
                                }
                    
                    # Continue the conversation with the tool results
                    continue
                else:
                    # Reset tool use tracking
                    tool_use_in_progress = False
                    tool_use_data = None
                    
                    # Add the assistant's response to the messages
                    request_body["messages"].append({
                        "role": "assistant",
                        "content": content
                    })
                    
                    # Ask for user input to continue the conversation
                    user_input = input("You: ")
                    
                    if user_input.lower() in ["exit", "quit"]:
                        break
                    
                    # Add the new user message
                    request_body["messages"].append({
                        "role": "user",
                        "content": user_input
                    })


if __name__ == "__main__":
    asyncio.run(main())
