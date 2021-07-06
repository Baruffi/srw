FROM python:3.9-alpine

WORKDIR /client

COPY settings/requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD python -u index.py
