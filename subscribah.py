from __future__ import unicode_literals

from os import environ
from uuid import uuid4

from flask import (
    Flask, render_template, redirect,
    flash, request, url_for
)
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from sqlalchemy_utils import UUIDType
from wtforms_alchemy import ModelForm


app = Flask(__name__)
app.config.update(
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='alex@reckerfamily.com',
    MAIL_PASSWORD=environ['SMTP_PASSWORD'],
    MAIL_DEFAULT_SENDER='alex@reckerfamily.com',
)

mail = Mail(app)
db = SQLAlchemy(app)


class Subscriber(db.Model):
    pk = db.Column(UUIDType(binary=False), primary_key=True, default=uuid4)

    email = db.Column(
        db.String(120),
        nullable=False,
        unique=True,
        info={'label': 'Email'}
    )

    verified = db.Column(db.Boolean, default=False)

    verify_key = db.Column(UUIDType(binary=False), default=uuid4)
    unsubscribe_key = db.Column(UUIDType(binary=False), default=uuid4)

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return '<Subscriber {}>'.format(self.email)

    def verify(self):
        if self.verified:
            return

        self.verified = True

    def send_verification_email(self):
        link = url_for('verify', key=self.verify_key, _external=True)
        return send_email(
            subject='Could you verify your email?',
            recipient=self.email,
            template='verify.msg',
            context={'link': link}
        )

    def send_newsletter_email(self, subject, message, connection):
        link = url_for('unsubscribe', key=self.unsubscribe_key, _external=True)
        return send_email(
            subject=subject,
            recipient=self.email,
            template='newsletter.msg',
            context={
                'link': link,
                'message': message
            },
            connection=connection
        )


class SubscriberForm(ModelForm):
    class Meta:
        model = Subscriber
        only = ['email']

    @classmethod
    def get_session(cls):
        return db.session


def send_email(subject, recipient, template, context={}, connection=None):
    connection = connection or mail
    connection.send(Message(
        subject=subject,
        recipients=[recipient],
        body=render_template(template, **context)
    ))


@app.route('/', methods=('GET', 'POST'))
def index():
    form = SubscriberForm(request.form)

    if request.method == 'POST':
        if form.validate():
            subscriber = Subscriber(form.data['email'])
            db.session.add(subscriber)
            db.session.commit()
            subscriber.send_verification_email()
            return redirect('/confirm/')

    for error in form.errors.get('email', []):
        flash(error)

    return render_template('index.html', form=form)


@app.route('/confirm/', methods=('GET', 'POST'))
def confirm():
    return render_template('confirm.html')


@app.route('/verify/<uuid:key>/')
def verify(key):
    subscriber = Subscriber.query.filter_by(verify_key=key).first_or_404()
    subscriber.verify()
    db.session.add(subscriber)
    db.session.commit()
    return render_template('verified.html')


@app.route('/unsubscribe/<uuid:key>/')
def unsubscribe(key):
    subscriber = Subscriber.query.filter_by(unsubscribe_key=key).first_or_404()
    db.session.delete(subscriber)
    db.session.commit()
    return render_template('unsubscribed.html')


if __name__ == '__main__':
    app.config.update(
        DEBUG=True,
        SECRET_KEY='mail-o-mail-it-never-fails',
        SERVER_NAME='127.0.0.1:5000',
        APPLICATION_ROOT=None,
        SQLALCHEMY_DATABASE_URI='sqlite:////tmp/test.db'
    )
    db.create_all()
    app.run()
