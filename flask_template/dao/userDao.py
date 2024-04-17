import psycopg2
from flask_template import connectionDB
from flask_template.others.format import rows_to_dict_list, responseJSON

class Login:
    def __init__(self):
        self.__conn = connectionDB()

    def __del__(self):
        if (self.__conn):
            self.__conn.close()

    def get_data_user_loader(self, id):
        """ Get data user for user_loader """
        try:
            with self.__conn.cursor() as cursor:
                query   =   """
                                SELECT                                                                 
                                    u_role
                                FROM 
                                    users
                                WHERE
                                    u_username = %(id)s                                
                            """
                params  = {
                    "id"      : id
                }
                cursor.execute(query, params)
                data    = rows_to_dict_list(cursor) 

            message = "Success get data user laoder"
            return responseJSON(200, "T", message, data)
        except psycopg2.Error as e:
            return responseJSON(400, "F", str(e), []) 
        
    def validate_user_login(self, username, password):
        """ Get data user for user_loader """
        try:
            with self.__conn.cursor() as cursor:
                query   =   """
                                SELECT                                 
                                    u_username,
                                    u_password,
                                    u_role,
                                    u_status
                                FROM 
                                    users
                                WHERE
                                    UPPER (u_username)  = UPPER (%(username)s)
                                    AND u_password      = %(password)s                               
                            """
                params  = {
                    "username"  : username,
                    "password"  : password
                }
                cursor.execute(query, params)
                data    = rows_to_dict_list(cursor) 

            message = "Success validate user login"
            return responseJSON(200, "T", message, data)
        except psycopg2.Error as e:
            return responseJSON(400, "F", str(e), []) 

