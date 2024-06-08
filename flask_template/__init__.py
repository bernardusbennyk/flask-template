import logging
import logging.handlers
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Load dotenv
load_dotenv()

# Create Flask app
app = Flask(__name__)
app.config.from_pyfile("settings.py")

# Initialize SQLAlchemy
db      = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)

# Initialize session login
login_manager = LoginManager(app)

# Handle session login redirect and message
login_manager.login_view                = "login"
login_manager.login_message             = "Please log in to access this page."
login_manager.login_message_category    = "danger"

# Initialize logging
log_format  = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s") 
handler     = logging.handlers.RotatingFileHandler("app.log", maxBytes=10485760, backupCount=2)
handler.setFormatter(log_format)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

# Declare route controller application
from flask_template.controllers import (routes, validate, user, dashboard)