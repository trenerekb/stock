import os


class Configuration(object):
    DEBUG = True
    # SECRET_KEY = 'dfgkmds65elkmwrnbnml546'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:bararus451@db_stock:5432'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:bararus451@localhost/stock'

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False



