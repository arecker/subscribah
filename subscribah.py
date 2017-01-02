from __future__ import unicode_literals

import os
from uuid import uuid4

from flask import Flask, render_template, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import UUIDType
from wtforms_alchemy import ModelForm


HERE = os.path.dirname(os.path.realpath(__file__))
DEFAULT_SETTINGS = os.path.join(HERE, 'config/default.py')

app = Flask(__name__)
app.config.from_pyfile(os.environ.get('SETTINGS_PATH', DEFAULT_SETTINGS))

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


class SubscriberForm(ModelForm):
    class Meta:
        model = Subscriber
        only = ['email']

    @classmethod
    def get_session(cls):
        return db.session


@app.route('/', methods=('GET', 'POST'))
def index():
    form = SubscriberForm(request.form)

    if request.method == 'POST':
        if form.validate():
            subscriber = Subscriber(form.data['email'])
            db.session.add(subscriber)
            db.session.commit()
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


@app.route('/remove/<uuid:key>/')
def unsubscribe(key):
    subscriber = Subscriber.query.filter_by(unsubscribe_key=key).first_or_404()
    db.session.delete(subscriber)
    db.session.commit()
    return render_template('unsubscribed.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
