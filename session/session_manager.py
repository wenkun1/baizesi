class SessionManager:

    def __init__(self):

        self.user_id = 1

        self.account_id = "test001"

        self.intent = None

        self.slots = {}

        self.finished = False

        self.register_mode = False
        self.register_slots = {}

        self.user_info = {}

    def reset(self):

        self.intent = None

        self.slots = {}

        self.finished = False
