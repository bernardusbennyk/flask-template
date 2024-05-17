from flask import abort, jsonify, render_template
from sqlalchemy.exc import OperationalError
from flask_template import app, db

@app.route("/health")
def health():            
    app_status  = "UP"
    try:
        db.engine.connect()
        db_status   = "UP"
    except OperationalError:
        db_status   = "DOWN"
    return jsonify({"app_status": app_status, "db_status": db_status})

@app.context_processor
def global_var():
    # Function global var for Jinja2    
    return dict(
        APP_NAME    = app.config["APP_NAME"],
        APP_INITIAL = app.config["APP_INITIAL"],
        COPYRIGHT   = app.config["COPYRIGHT"],
        VERSION     = app.config["VERSION"]
    )

@app.errorhandler(403)
def handle_forbidden(e):
    return render_template("errors/403.html")

@app.errorhandler(404)
def handle_bad_request(e):
    return render_template("errors/404.html")

@app.errorhandler(405)
def handle_method_not_allowed(e):
    return render_template("errors/405.html")

@app.errorhandler(500)
def handle_internal_server_error(e):    
    return render_template("errors/500.html")
