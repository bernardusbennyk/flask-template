import logging, psycopg2
import logging.handlers
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager

# Load dotenv
load_dotenv()

# Create Flask app
app = Flask(__name__)
app.config.from_pyfile("settings.py")

# Initialize session login
login_manager = LoginManager()
login_manager.init_app(app)

# Handle session login redirect and message
login_manager.login_view                = "login"
login_manager.login_message             = "Please log in to access this page."
login_manager.login_message_category    = "danger"

# Initialize logging
log_format  = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s") 
handler     = logging.handlers.RotatingFileHandler("app.log", maxBytes=10000, backupCount=1)
handler.setFormatter(log_format)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

def connectionDB():    
    conn = psycopg2.connect(
        host        = app.config["HOST_DB"],
        database    = app.config["SID_DB"],
        port        = app.config["PORT_DB"],
        user        = app.config["USER_DB"],
        password    = app.config["PASSWORD_DB"]
    )
    return conn

# Declare route controller application
from flask_template.controllers import (routes, validate, user)