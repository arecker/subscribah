from os import environ

from subscribah import app, db

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'postgresql://'
    '{user}:{password}@'
    '{host}:{port}/{table}'
).format(user='postgres', password=environ['DB_PASSWORD'],
         host='db', port='5432', table='subscriber')

db.create_all()
