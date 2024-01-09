FROM python:3.11

RUN apt-get update

WORKDIR /app/

COPY requirements.txt ./
COPY /.env/ ./

RUN pip install -r requirements.txt

EXPOSE 5000

CMD flask run --debug --host=0.0.0.0
