#!/usr/bin/env bash

cd /app

python <<- EOM
from subscribah import db
db.create_all()
EOM

gunicorn --bind 0.0.0.0:80 subscribah:app
