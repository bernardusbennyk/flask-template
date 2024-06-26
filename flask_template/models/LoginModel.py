from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username):    
        self.id         = id
        self.username   = username          

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True