#config/config.py
import os
class Config(object):
    #Common configuration used by all the environments (dev, testing, prod)
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Default URI to use postgreSQL env variables
    #SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db/{os.getenv('POSTGRES_DB')}")
    
class Development(Config):
    #Config related to development environment
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///development.db')
    
class Testing(Config):
    #Config related to testing environment
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
    # Overiding the DATABASE_URI for a testing db
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///testing.db')
class Production(Config):
    #Config related to production environment
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///production.db'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql://username:password@hostname:port/database_name')