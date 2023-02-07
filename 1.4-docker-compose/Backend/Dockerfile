FROM python:3.9.6-alpine

WORKDIR site
COPY ./stocks_products .
COPY ./Gunicorn_settings /etc/systemd/system

RUN pip3 install -r requirements.txt
#RUN python manage.py migrate

EXPOSE 8000
