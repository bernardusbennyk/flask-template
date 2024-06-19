import bcrypt, traceback
from sqlalchemy.engine.row import Row
from sqlalchemy.exc import IntegrityError, OperationalError, ProgrammingError, SQLAlchemyError
from flask_template import app

def rows_to_dict(rows):
    """ Format select query as column and value from database in dictionary """        
    if (isinstance(rows, list)):        
        return [rows_to_dict(row) for row in rows]
    elif (isinstance(rows, Row)):
        return rows._asdict()
    else:
        return rows

def responseJSON(status_code, status, message, result):
    """ Format response """
    return {
        "status_code"   : status_code, 
        "status"        : status, 
        "message"       : message, 
        "result"        : result
    }

def hash_password(password):       
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(12))

def verify_password(password, hashed_password):                
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)    

def execute_db(db_operation, success_message, default_data, *args, **kwargs):
    data    = default_data
    try:
        result  = db_operation(*args, **kwargs)        
        if result:
            data    = rows_to_dict(result)
        message = success_message
        return responseJSON(200, "T", message, data)
    except OperationalError as e:
        app.logger.error(traceback.format_exc())
        message = f"Operational error: {e}"        
        return responseJSON(500, "F", message, data)
    except (ProgrammingError, IntegrityError) as e:
        app.logger.error(traceback.format_exc())
        message = f"Syntax error: {e}"        
        return responseJSON(400, "F", message, data)
    except SQLAlchemyError as e:
        app.logger.error(traceback.format_exc())
        message = f"Database error: {e}"        
        return responseJSON(500, "F", message, data)    
    except Exception as e:
        app.logger.error(traceback.format_exc())
        message = f"Error: {e}"        
        return responseJSON(500, "F", message, data)