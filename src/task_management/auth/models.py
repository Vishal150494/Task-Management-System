#src/task_management/auth/models.py
"""
This model will represent users in the application & 
provide fields for 'username', 'email', 'password hash'.
"""
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from ..db import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    """
    User model for storing user information
    """
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True, nullable=False)
    email_id = db.Column(db.String(128), index=True, unique=True, nullable=False)
    password = db.Column(db.String(128), unique=True, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        """
        Standard python Method to return a string representation of the user object that includes the username. 
        """
        return f"<User {self.username}:{self.email_id}>"
    
    def create_password(self, password):
        """
        Method to generate and set the password hash from the provided password.
        """
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        """
        Method to check if the provided password matches the stored password hash (<password>).
        """
        return check_password_hash(self.password, password)
