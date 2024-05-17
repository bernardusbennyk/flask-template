import bcrypt

def rows_to_dict(rows):
    """ Format select query as column and value from database in dictionary """    
    if (isinstance(rows, list)):        
        return [rows_to_dict(row) for row in rows]
    else:
        return rows._asdict()

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