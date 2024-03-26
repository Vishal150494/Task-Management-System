#src/main.py
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, flash, redirect, url_for, send_from_directory
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from flask_login import LoginManager
from src.task_management.auth.models import User
from src.task_management.auth.routes import auth_bp
from src.task_management.tasks.routes import task_bp
from src.task_management.db import db, init_app as init_db
from config.config import Development, Testing, Production

log_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
if not os.path.exists(log_directory):
    os.makedirs(log_directory)
    
log_file_path = os.path.join(log_directory, 'app.log')

def create_web_app():
    """This is an application factory method to support different configs easily"""
    config_mapping = {
        'dev': Development,
        'test': Testing,
        'prod': Production
    }
    config_class = config_mapping.get(os.environ.get('FLASK_ENV'), Development) # Setting Development config class as default if nothing is specified.
    app = Flask('Task Management', template_folder='src/templates', static_folder='src/static')
    CORS(app)
    app.config.from_object(config_class)
    
    #Initializing db & migrations
    init_db(app)
    
    # Initialize logging
    if app.debug:
        handler = RotatingFileHandler(log_file_path, maxBytes=100000, backupCount=1)
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)

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
    
    # Swagger UI setup
    SWAGGER_URL = '/api/docs' # URL to access Swagger UI
    API_URL = '/static/swagger.json' # URL to access OpenAPI specification
    swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={"app_name":"Task Management API"})
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    # Registering my blueprints for auth & tasks modules
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(task_bp, url_prefix='/tasks')
    
    # Serving OpenAPi spec file from the static directory.
    @app.route('/static/swagger.json')
    def serve_swagger_json():
        return send_from_directory(app.static_folder, 'swagger.json')
    
    return app

app = create_web_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
