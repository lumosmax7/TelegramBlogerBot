class UserStateHandler:
    def __init__(self):
        self.current_state = None
        self.current_draft = None

    def set_user_state(self, state):
        self.current_state = state

    def set_user_draft(self, draft):
        self.current_draft = draft

    def get_user_state(self):
        return self.current_state

    def get_user_draft(self):
        return self.current_draft