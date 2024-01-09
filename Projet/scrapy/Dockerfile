FROM python:3.11

RUN apt-get update

WORKDIR /app/

COPY requirements.txt ./
COPY /env/ ./

RUN pip install -r requirements.txt

CMD cd newscrawler/newscrawler/spiders && scrapy crawl nba_player
