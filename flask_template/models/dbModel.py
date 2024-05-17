import uuid
from sqlalchemy.dialects.postgresql import UUID
from flask_template import db

class User(db.Model):
    __tablename__ = 'users'

    id          = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username    = db.Column(db.String(12), unique=True, nullable=False)
    password    = db.Column(db.LargeBinary, nullable=False)    
    is_active   = db.Column(db.Boolean, nullable=False, default=True)
    created_at  = db.Column(db.DateTime, nullable=False, default=db.func.now())
    created_by  = db.Column(db.String(12), nullable=False)
    updated_at  = db.Column(db.DateTime, nullable=True, onupdate=db.func.now())
    updated_by  = db.Column(db.String(12), nullable=True)     

    def __repr__(self):
        return f"<User {self.username}>"
    