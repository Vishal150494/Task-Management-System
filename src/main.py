#src/main.py
import os
from flask import Flask, flash, redirect, url_for
from flask_login import LoginManager
from src.task_management.auth.models import User
from src.task_management.auth.routes import auth_bp
from src.task_management.tasks.routes import task_bp
from src.task_management.db import db, init_app as init_db
from config.config import Development, Testing, Production, Config
from flask_wtf import CSRFProtect

def create_web_app():
    """This is an application factory method to support different configs easily"""
    config_mapping = {
        'dev': Development,
        'test': Testing,
        'prod': Production
    }
    config_class = config_mapping.get(os.environ.get('FLASK_ENV'), Development) # Setting Development config class as default if nothing is specified.
    app = Flask('Task Management', template_folder='src/templates')
    app.config.from_object(config_class)
    
    #app.secret_key = app.config.get('SECRET_KEY')
    
    #Initializing CSRF protection
    #csrf = CSRFProtect(app)
    
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
    
    return app

app = create_web_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    
    