import boto3
import json

# 创建 Bedrock Runtime 客户端
bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-west-2'
)

# 单轮对话：使用 InvokeModel API
def invoke_claude(prompt):
    response = bedrock_runtime.invoke_model(
        modelId='us.anthropic.claude-3-5-sonnet-20241022-v2:0',  # Sonnet 3.5 v2
        # 或使用 'us.anthropic.claude-3-7-sonnet-20250219-v1:0' 表示 Sonnet 3.7
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        })
    )
    
    response_body = json.loads(response['body'].read())
    return response_body['content'][0]['text']

# 多轮对话：使用 Converse API
def converse_with_claude(messages):
    # 确保消息格式正确
    formatted_messages = []
    for msg in messages:
        if msg["role"] == "user":
            formatted_messages.append({
                "role": "user",
                "content": [{"text": msg["content"]}]
            })
        elif msg["role"] == "assistant":
            formatted_messages.append({
                "role": "assistant",
                "content": [{"text": msg["content"]}]
            })
    
    response = bedrock_runtime.converse(
        modelId='us.anthropic.claude-3-5-sonnet-20241022-v2:0',  # Sonnet 3.5 v2
        messages=formatted_messages
    )
    
    return response['output']['message']['content'][0]['text']

# 示例使用
try:
    print("正在测试单轮对话...")
    result = invoke_claude("解释量子计算的基本原理")
    print("单轮对话结果:")
    print(result)
    print("\n" + "-"*50 + "\n")
    
    print("正在测试多轮对话...")
    # 多轮对话示例
    conversation = converse_with_claude([
        {"role": "user", "content": "你好，请介绍一下自己"}
    ])
    print("多轮对话第一轮结果:")
    print(conversation)
    
    # 继续对话
    conversation2 = converse_with_claude([
        {"role": "user", "content": "你好，请介绍一下自己"},
        {"role": "assistant", "content": conversation},
        {"role": "user", "content": "你能用 Python 写一个简单的网页爬虫吗？"}
    ])
    print("\n多轮对话第二轮结果:")
    print(conversation2)
    
except Exception as e:
    print(f"发生错误: {str(e)}")
