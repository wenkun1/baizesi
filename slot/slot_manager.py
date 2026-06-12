# slot/slot_manager.py

class SlotManager:

    @staticmethod
    def merge(old_slot, new_slot):

        for k, v in new_slot.items():

            if v:
                old_slot[k] = v

        return old_slot

    # 获取缺失的槽位 
    @staticmethod
    def missing_slots(
            intent,
            current_slot,
            config
    ):

        required = config.get(
            intent,
            []
        )

        missing = []

        for item in required:

            if not current_slot.get(item):
                missing.append(item)

        return missing