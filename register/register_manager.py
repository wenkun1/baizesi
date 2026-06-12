from register.register_config import (
    REGISTER_SLOTS,
    REGISTER_QUESTION
)


class RegisterManager:

    @staticmethod
    def get_missing(register_slots):

        missing = []

        for field in REGISTER_SLOTS:

            if not register_slots.get(field):

                missing.append(field)

        return missing

    @staticmethod
    def next_question(register_slots):

        missing = RegisterManager.get_missing(
            register_slots
        )

        if not missing:
            return None

        return REGISTER_QUESTION[
            missing[0]
        ]