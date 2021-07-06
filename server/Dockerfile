FROM python:3.9-alpine

WORKDIR /server

COPY settings/requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN mkdir local

COPY . .

CMD python -u index.py
