from openai import OpenAI

client = OpenAI(
    base_url="http://58.56.4.133:11434/v1",
    api_key="sk-no-api-key"
)

MODEL_NAME = ""


def chat(prompt: str) -> str:

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "你是专业助手，只返回JSON"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content