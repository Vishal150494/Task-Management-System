# src/task_management/db.py
"""
We are setting up databse connection and SQLAlchenmy object.
Tis setup will be imported later in the other model definitions to create model classes. 
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate =   None # Declaring migration

def init_app(app):
    global migrate
    db.init_app(app)
    migrate = Migrate(app,db) # Initializing migrate with app & my db
