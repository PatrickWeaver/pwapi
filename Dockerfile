FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /pwapi
WORKDIR /pwapi
ADD requirements.txt /pwapi/
RUN pip install -r requirements.txt
ADD . /pwapi/

EXPOSE 8000

CMD ["/pwapi/start.sh"]
