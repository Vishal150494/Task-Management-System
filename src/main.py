#src/main.py
from flask import Flask, flash, redirect, url_for
from flask_login import LoginManager
from src.task_management.auth.models import User
from src.task_management.auth.routes import auth_bp
from src.task_management.tasks.routes import task_bp
from src.task_management.db import db, init_app as init_db

app = Flask("Task Management")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Initializing db & migrations
init_db(app)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    """This method is essential in reloading the user object from the session"""
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized_user():
    """This method handles unauthorized user requests"""
    flash("You must be logged in to access this page.", "FAILED!")
    return redirect(url_for('auth.login'))

# Registering my blueprints for auth & tasks modules
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(task_bp, url_prefix='/tasks')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    
    