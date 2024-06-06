FROM python:3.8-buster

ENV PYTHONBUFFERD=1

WORKDIR /django

COPY requirments.txt requirments.txt

RUN pip install -r requirments.txt

COPY . .

CMD py manage.py runserver 0.0.0.0:8000