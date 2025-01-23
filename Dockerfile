FROM python:3.10.12-alpine

WORKDIR /usr/src/app
ADD . /usr/src/app

RUN pip install -r requirements.txt
