class UserStateHandler:
    def __init__(self):
        self.current_state = None
        self.current_draft = None
        self.current_post = None
        self.current_file_name = None

    def set_user_state(self, state):
        self.current_state = state

    def set_user_draft(self, draft):
        self.current_draft = draft

    def set_user_post(self,post):
        self.current_post = post

    def set_user_file_name(self, file_name):
        self.current_file_name = file_name

    def get_user_state(self):
        return self.current_state

    def get_user_draft(self):
        return self.current_draft

    def get_user_post(self):
        return self.current_post

    def get_user_file_name(self):
        return self.current_file_name