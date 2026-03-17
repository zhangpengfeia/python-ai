from openai import OpenAI

try:
    client = OpenAI(
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为: api_key="sk-xxx",
        api_key="ollama",
        base_url="http://localhost:11434/v1",
    )

    completion = client.chat.completions.create(
        model="qwen3:4b",  # 模型列表: https://help.aliyun.com/model-studio/getting-started/models
        messages=[
            {'role': 'system', 'content': '你是Javascript专家，不喜欢说废话'},
            {'role': 'assistant', 'content': '好的，我是编程专家，并且话不多，你要问什么？'},
            {'role': 'user', 'content': '输出1-10的数字'}
        ],
        stream=True
    )
    for chunk in completion:
        print(
            chunk.choices[0].delta.content,
            end="",
            flush=True
        )

except Exception as e:
    print(f"错误信息：{e}")
    print("请参考文档：https://help.aliyun.com/model-studio/developer-reference/error-code")