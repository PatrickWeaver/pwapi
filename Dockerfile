FROM python:3

COPY requirements.txt /
RUN pip install -r ./requirements.txt

RUN mkdir -p /var/www/app
WORKDIR /var/www/app

COPY app/ /var/www/app

ENV FLASK_APP=app.py

EXPOSE 5000

CMD flask db upgrade && flask run -h 0.0.0.0 -p 5000
