# intent/intent_recognizer.py

import json

from llm.client import chat
from prompt.intent_prompt import INTENT_PROMPT
from intent.intent_config import INTENT_NAME_MAP

class IntentRecognizer:

    @staticmethod
    def recognize(text):

        prompt = INTENT_PROMPT.format(
            intent_list=INTENT_NAME_MAP,
            query=text
        )
        print("\n==========Prompt==========")
        print(prompt)

        result = chat(prompt)

        return json.loads(result)