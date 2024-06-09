class Entity:
    def __init__(self, username):
        self.username = username

class Sessions:
    def __init__(self):
        self.sessions = {}

    def get_token(self, token):
        return self.sessions.get(token)

    def validate_token(self, token):
        # This method should implement the actual validation logic
        return token in self.sessions

    def issue_new_token(self, username):
        import uuid
        token = str(uuid.uuid4())
        self.sessions[token] = Entity(username)
        return token