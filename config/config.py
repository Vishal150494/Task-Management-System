#config/config.py

class Config(object):
    #Common configuration used by all the environments (dev, testing, prod)
    SECRET_KEY = 'Vishal1234.!'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class Development(Config):
    #Config related to development environment
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    DEBUG = True
    
class Testing(Config):
    #Config related to testing environment
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
    
class Production(Config):
    #Config related to production environment
    SQLALCHEMY_DATABASE_URI = 'sqlite:///production.db'