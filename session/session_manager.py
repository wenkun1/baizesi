class SessionManager:

    def __init__(
            self,
            account_id="test001",
            user_id=1,
            user_info=None
    ):

        self.user_id = user_id

        self.account_id = account_id

        self.intent = None

        self.slots = {}

        self.finished = False

        self.register_mode = False
        self.register_slots = {}

        self.user_info = user_info or {}

    def reset(self):

        self.intent = None

        self.slots = {}

        self.finished = False
