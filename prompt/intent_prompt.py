# intent/intent_prompt.py
INTENT_PROMPT = """
你是意图识别助手。

意图列表：
{intent_list}

请根据用户输入，识别意图，并返回意图名称。
示例返回格式：

{{
    "intent":"leave"
}}

用户输入：
{query}
"""