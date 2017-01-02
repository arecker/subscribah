FROM python:2.7
MAINTAINER Alex Recker <alex@reckerfamily.com>

RUN mkdir -p /app
COPY requirements.txt /app
RUN pip install -r /app/requirements.txt

COPY subscribah.py /app
COPY templates /app/templates
COPY config /app/config
COPY entry.sh /

COPY newsletter.py /app

EXPOSE 80
ENV SETTINGS_PATH='/app/config/prod.py'
ENTRYPOINT ["/entry.sh"]
