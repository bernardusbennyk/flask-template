from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, login_required
from hashlib import md5
from flask_template import app, login_manager
from flask_template.models.userModel import User
from flask_template.controllers.validate import login_not_allowed
from flask_template.dao.userDao import Login

@login_manager.user_loader
def load_user(user_id):
    """ Load session user """    
    login   = Login()
    try:
        v_get_data_user_loader = login.get_data_user_loader(user_id)
        # If user not exists or error return None
        if (v_get_data_user_loader["status"] == "F" or not v_get_data_user_loader["result"]): 
            app.logger.error(f"DAO get_data_user_loader: {v_get_data_user_loader['message']}")
            return None

        # Set session user    
        username    = user_id
        user_role   = v_get_data_user_loader["result"][0]["u_role"]
        return User(username, user_role)
    except Exception as e:
        app.logger.error(f"Controller load_user: {e}")
        abort(500, str(e))
    finally:
        del login

@app.route("/login", methods=["GET", "POST"])
@login_not_allowed
def login():
    # Load login page
    if request.method == "GET":                              
        # For highlight invalid form
        validate    = request.args.getlist("validate")

        # Set username value back to form
        username    = request.args.get("username", "")

        return render_template("login.html", menu="Login", username=username, validate=validate)
    
    # Process log in
    elif request.method == "POST":
        login   = Login()
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
            
            # Hash password with md5
            password    = md5(password.encode()).hexdigest()

            # Validate user login
            v_validate_user_login   = login.validate_user_login(username, password)
            if (v_validate_user_login["status"] == "F"):
                app.logger.error(f"DAO validate_user_login: {v_validate_user_login['message']}")
                message     = v_validate_user_login["message"]
                flash_type  = "error"
                flash(message, flash_type)
                return redirect(url_for("login"))
            elif (not v_validate_user_login["result"]):
                message     = "Username and password not match."
                flash_type  = "danger"
                flash(message, flash_type)
                return redirect(url_for("login", username=username))
            
            # Set user data        
            v_username      = v_validate_user_login["result"][0]["u_username"] 
            v_role          = v_validate_user_login["result"][0]["u_role"]
            v_status_user   = v_validate_user_login["result"][0]["u_status"]

            # Check status user active or inactive 
            if (v_status_user == "F"):
                message     = "Account deactivated."
                flash_type  = "info"
                flash(message, flash_type)
                return redirect(url_for("login"))
            
            # Set session user loader
            user    = User(v_username, v_role)        
            login_user(user)                               
            return redirect(url_for("home"))
        except Exception as e:
            app.logger.error(f"Controller login (POST): {e}")
            abort(500, str(e))
        finally:
            del login

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))
