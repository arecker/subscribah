FROM python:2.7
MAINTAINER Alex Recker <alex@reckerfamily.com>

RUN mkdir -p /app
COPY requirements.txt /app
RUN pip install -r /app/requirements.txt

COPY subscribah.py /app
COPY templates /app/templates
COPY entry.sh /

EXPOSE 80
ENTRYPOINT ["/entry.sh"]
