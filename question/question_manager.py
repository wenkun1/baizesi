# question/question_manager.py

from question.question_config import QUESTION_MAP


class QuestionManager:

    @staticmethod
    def generate(missing_slots):

        if not missing_slots:
            return None

        slot = missing_slots[0]

        return QUESTION_MAP.get(
            slot,
            f"请补充{slot}"
        )