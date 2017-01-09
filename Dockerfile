FROM python:2.7
MAINTAINER Alex Recker <alex@reckerfamily.com>

RUN mkdir -p /app
COPY requirements.txt /app
RUN pip install -r /app/requirements.txt

COPY subscribah.py /app
COPY templates /app/templates
COPY wsgi.py /app

COPY newsletter.py /app

EXPOSE 80
WORKDIR /app
ENTRYPOINT ["gunicorn"]
CMD ["--bind", "0.0.0.0:80", "wsgi:application"]
