FROM python:3

RUN mkdir -p /var/www/app
WORKDIR /var/www/app

COPY . /var/www/app

ENV FLASK_APP pwapi

RUN pip install -e .

EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["pwapi"]
