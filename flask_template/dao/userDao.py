from sqlalchemy.exc import IntegrityError, OperationalError, ProgrammingError, SQLAlchemyError
from flask_template import db
from flask_template.models.dbModel import User
from flask_template.others.utils import responseJSON, rows_to_dict

def get_data_user_loader(id):    
    data    = {}
    try:        
        query   = db.session.query(
                    User.id.label("id"), 
                    User.username
                ).filter(
                    User.id == id
                ).first()        
        if (query):           
            data    = rows_to_dict(query)
        message = "Success get data user loader"
        
        return responseJSON(200, "T", message, data)    
    except OperationalError as e:
        message = f"Database connection error: {e}"        
        return responseJSON(500, "F", message, data)
    except (ProgrammingError, IntegrityError) as e:
        message = f"Error executing query: {e}"        
        return responseJSON(400, "F", message, data)
    except SQLAlchemyError as e:
        message = f"Error query: {e}"        
        return responseJSON(500, "F", message, data)
    except Exception as e:
        message = f"Error: {e}"        
        return responseJSON(500, "F", message, data)
    
def get_data_user_login(username):     
    data    = {}
    try:        
        query   = db.session.query(
                    User.id,
                    User.password, 
                    User.is_active                    
                ).filter(
                    User.username == username
                ).first()               
        if (query):                       
            data    = rows_to_dict(query)                                    
        message = "Success get data user login"            
        
        return responseJSON(200, "T", message, data)    
    except OperationalError as e:
        message = f"Database connection error: {e}"        
        return responseJSON(500, "F", message, data)
    except (ProgrammingError, IntegrityError) as e:
        message = f"Error executing query: {e}"        
        return responseJSON(400, "F", message, data)
    except SQLAlchemyError as e:
        message = f"Error query: {e}"        
        return responseJSON(500, "F", message, data)
    except Exception as e:
        message = f"Error: {e}"        
        return responseJSON(500, "F", message, data)
