def get_application():
    from os import environ
    from subscribah import db, app
    app.config.update(
        DEBUG=False,
        SECRET_KEY=environ['SECRET_KEY'],
        SERVER_NAME=environ.get('SERVER_NAME', 'alexrecker.com'),
        APPLICATION_ROOT='/subscribe/',
        SQLALCHEMY_DATABASE_URI='postgresql://postgres:{}@db:5432/subscriber'.format(environ['DB_PASSWORD']),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    db.create_all()
    return app

application = get_application()
