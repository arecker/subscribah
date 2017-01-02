from os import environ

DEBUG = False
SECRET_KEY = environ['SECRET_KEY']
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:{}@db:5432/subscriber'.format(environ['DB_PASSWORD'])
