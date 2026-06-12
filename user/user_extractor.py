import json

from llm.client import chat
from prompt.user_prompt import USER_PROMPT


class UserExtractor:

    @staticmethod
    def extract(text):

        prompt = USER_PROMPT.format(
            text=text
        )

        result = chat(prompt)

        return json.loads(result)