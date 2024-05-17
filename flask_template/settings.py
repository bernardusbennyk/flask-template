import os

# Config application
SECRET_KEY  = "yuJMp7^BZVaHAeo!"
APP_NAME    = "Flask Template"
APP_INITIAL = "FT"
COPYRIGHT   = "2023"
VERSION     = "1.0.0"

# Config database
HOST_DB     = os.getenv("host_db")
SID_DB      = os.getenv("sid_db")
PORT_DB     = os.getenv("port_db")
USER_DB     = os.getenv("user_db")
PASSWORD_DB = os.getenv("password_db")
# Config SQLAlchemy
SQLALCHEMY_DATABASE_URI         = f"postgresql://{USER_DB}:{PASSWORD_DB}@{HOST_DB}:{PORT_DB}/{SID_DB}"
SQLALCHEMY_TRACK_MODIFICATIONS  = False