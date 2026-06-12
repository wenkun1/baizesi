# slot/slot_extractor.py

import json

from llm.client import chat
from prompt.slot_prompt import SLOT_PROMPT

class SlotExtractor:
    @staticmethod
    def extract(
            intent,
            slots,
            history,
            text,
            missing_slots
    ):

        prompt = SLOT_PROMPT.format(
            intent=intent,
            slots=slots,
            history=history,
            text=text,
            missing_slots=missing_slots
        )

        result = chat(prompt)

        print("\n==========LLM返回==========")
        print(result)
        print("==========================\n")

        try:
            return json.loads(result)
        except Exception as e:

            print("JSON解析失败:", e)

            return {}
