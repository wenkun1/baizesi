# workflow/workflow_engine.py

from intent.intent_recognizer import IntentRecognizer

from slot.slot_config import INTENT_SLOTS

from slot.slot_extractor import SlotExtractor

from slot.slot_manager import SlotManager

from question.question_manager import QuestionManager

from storage.db import DB


class WorkflowEngine:

    def __init__(self):

        self.db = DB()


    def process(
            self,
            session,
            text
    ):
        if session.intent is None:

            result = IntentRecognizer.recognize(text)

            session.intent = result.get("intent")

            if session.intent == "other" or not session.intent:
                session.reset()
                return {
                    "finish": False,
                    "reply": "暂不支持该业务类型，请重新描述需求。"
                }
            
        missing = SlotManager.missing_slots(
            session.intent,
            session.slots,
            INTENT_SLOTS
        )

        slots = SlotExtractor.extract(
            session.intent,
            INTENT_SLOTS[session.intent],
            session.slots,
            text,
            missing
        )

        session.slots = SlotManager.merge(
            session.slots,
            slots
        )

        missing = SlotManager.missing_slots(
            session.intent,
            session.slots,
            INTENT_SLOTS
        )

        if missing:

            return {
                "finish": False,
                "reply": QuestionManager.generate(missing)
            }
        self.db.save_order(
            session.user_id,
            session.intent,
            session.slots
        )

        session.finished = True
        reply = f"提交成功：{session.slots}"
        session.reset()

        return {
            "finish": True,
            "reply": reply
        }