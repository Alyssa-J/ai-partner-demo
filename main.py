import os
from openai import OpenAI

#创建与大模型交互的客户端对象（DEEPSEEK_API_KEY为环境变量的名字，值是apikey的值）
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com/")

response = client.chat.completions.create(
    model = "deepseek-v4-pro",
    messages=[
        {"role":"system","content":"你是一个知识百科助手，名字叫做嫌疑猫。"},
        {"role":"user","content":"你是谁，你能帮我做什么？"},
    ],
    stream=False,
    reasoning_effort="high",
    extra_body={"thinking":{"type":"enabled"}}
)
#输出大模型的返回结果
print(response.choices[0].message.content)