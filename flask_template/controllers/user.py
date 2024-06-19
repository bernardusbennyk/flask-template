import traceback
from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, login_required
from flask_template import app, login_manager
from flask_template.controllers.validate import login_not_allowed
from flask_template.models.LoginModel import User
from flask_template.others.utils import verify_password, hash_password
from flask_template.dao.userDao import get_data_user_loader, get_data_user_login

@login_manager.user_loader
def load_user(user_id):
    """ Load session user """       
    try:        
        v_get_data_user_loader  = get_data_user_loader(user_id)        
        # If user not exists or error return None
        if (v_get_data_user_loader["status"] == "F" or not v_get_data_user_loader["result"]):                  
            return None
        
        # Set session user    
        id          = user_id
        username    = v_get_data_user_loader["result"]["username"]
        return User(id, username)
    except Exception as e:
        app.logger.error(f"load_user: {traceback.format_exc()}")
        abort(500, str(e))

@app.route("/", methods=["GET"])
@app.route("/login", methods=["GET", "POST"])
@login_not_allowed
def login():
    # Load login page
    if request.method == "GET":   
        try:                           
            # For highlight invalid form
            validate    = request.args.getlist("validate")

            # Set username value back to form
            username    = request.args.get("username", "")

            return render_template("login.html", menu="Login", username=username, validate=validate)
        except Exception as e:
            app.logger.error(f"render login: {traceback.format_exc()}")
            abort(500, str(e))
    
    # Process log in
    elif request.method == "POST":        
        try:            
            username    = request.form.get("username", None)
            password    = request.form.get("password", None)            

            # Validate input data
            validate    = []
            if (username in [None, ""]):
                validate.append("username")            
            if (password in [None, ""]):
                validate.append("password")            
            if (validate):
                message     = f"<strong>{', '.join(validate)}</strong> must not be empty."
                flash_type  = "danger"
                flash(message, flash_type)
                return redirect(url_for("login", validate=validate))
            
            # Get data user login                        
            v_get_data_user_login   = get_data_user_login(username)                                 
            if (v_get_data_user_login["status"] == "F"):                
                message     = v_get_data_user_login["message"]
                flash_type  = "error"
                flash(message, flash_type)
                return redirect(url_for("login"))
            elif (not v_get_data_user_login["result"]):
                message     = f"User {username} not found"
                flash_type  = "danger"
                flash(message, flash_type)
                return redirect(url_for("login"))

            # Set data user from database
            user_id         = v_get_data_user_login["result"]["id"]
            hash_password   = v_get_data_user_login["result"]["password"]
            user_is_active  = v_get_data_user_login["result"]["is_active"]

            # Verify password with bcrypt            
            validate_password   = verify_password(password, hash_password)
            
            if (validate_password is False):
                message     = "Username and password doesn't match"
                flash_type  = "danger"
                flash(message, flash_type)
                return redirect(url_for("login"))
            
            # Check status user active or inactive
            if (user_is_active is False):
                message     = "Account deactivated"
                flash_type  = "info"
                flash(message, flash_type)
                return redirect(url_for("login"))

            # Set session user loader
            user    = User(user_id, username)        
            login_user(user)                                           
            return redirect(url_for("dashboard"))
        except Exception as e:
            app.logger.error(f"login: {traceback.format_exc()}")
            abort(500, str(e))                

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    try:
        logout_user()
        return redirect(url_for("login"))
    except Exception as e:
        app.logger.error(f"logout: {traceback.format_exc()}")
        abort(500, str(e))

@app.route("/addUser", methods=["GET"])
def addUser():
    from flask_template import db     
    from flask_template.models.dbModel import User    
        
    hash_pw = hash_password("asdjklal")    
    new_user = User(
        username='admin',     
        password=hash_pw,
        created_by='root'
    )         
    db.session.add(new_user)
    db.session.commit()
    return {"message": "Add user successful"}

@app.route("/updateUser", methods=["GET"])
def updateUser():
    from flask_template import db     
    from flask_template.models.dbModel import User    
        
    result = db.session.query(User) \
        .filter(User.username == "admin", 
                User.is_active == True) \
        .update({"is_active": False})   
    db.session.commit()     
    return {"message": f"Update {result} user success"}
