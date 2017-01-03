from os import environ

DEBUG = False
SECRET_KEY = environ['SECRET_KEY']
SERVER_NAME = environ.get('SERVER_NAME', 'alexrecker.com')
APPLICATION_ROOT = '/subscribe/'
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:{}@db:5432/subscriber'.format(environ['DB_PASSWORD'])
SQLALCHEMY_TRACK_MODIFICATIONS = False
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = environ['SMTP_USER']
MAIL_PASSWORD = environ['SMTP_PASSWORD']
MAIL_DEFAULT_SENDER = 'alex@reckerfamily.com'
