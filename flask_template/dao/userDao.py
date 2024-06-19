import traceback
from sqlalchemy.exc import IntegrityError, OperationalError, ProgrammingError, SQLAlchemyError
from flask_template import app, db
from flask_template.others.utils import responseJSON, rows_to_dict
from flask_template.models.dbModel import User

def get_data_user_loader(id):
    data    = {}
    try:
        result  = db.session.query(
                    User.id.label("id"), 
                    User.username
                ).filter(
                    User.id == id
                ).first()
        if (result):
            data  = rows_to_dict(result)
        message = "Success get data user loader"        
        return responseJSON(200, "T", message, data)
    except (OperationalError, IntegrityError, SQLAlchemyError) as e:        
        app.logger.error(traceback.format_exc())
        message = f"Database error: {e}"        
        return responseJSON(500, "F", message, data)    
    except Exception as e:        
        app.logger.error(traceback.format_exc())
        message = f"Error: {e}"        
        return responseJSON(500, "F", message, data)
    
def get_data_user_login(username):
    data    = {}
    try:
        result      = db.session.query(
                        User.id,
                        User.password, 
                        User.is_active                   
                    ).filter(
                        User.username == username
                    ).first()
        if (result):
            data    = rows_to_dict(result)
        message     = "Success get data user login"
        return responseJSON(200, "T", message, data)
    except (ProgrammingError, OperationalError, IntegrityError, SQLAlchemyError) as e:            
        app.logger.error(traceback.format_exc())
        message = f"Database error: {e}"        
        return responseJSON(500, "F", message, data)    
    except Exception as e:        
        app.logger.error(traceback.format_exc())
        message = f"Error: {e}"        
        return responseJSON(500, "F", message, data)
    