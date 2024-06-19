from flask_template import db
from flask_template.models.dbModel import User
from flask_template.others.utils import execute_db

class Login:
    def sql_get_data_user_login(self):
        result   = db.session.query(
                    User.id,
                    User.password, 
                    User.is_active                    
                ).filter(
                    User.username == self._username
                ).first()
        return result
    
    def sql_get_data_user_loader(self):
        result   = db.session.query(
                    User.id.label("id"), 
                    User.username
                ).filter(
                    User.id == self._id
                ).first()
        return result        
    
    def get_data_user_login(self, username):
        self._username  = username
        return execute_db(self.sql_get_data_user_login, "Success get data user login", {})
    
    def get_data_user_loader(self, id):
        self._id    = id
        return execute_db(self.sql_get_data_user_loader, "Success get data user loader", {})
    