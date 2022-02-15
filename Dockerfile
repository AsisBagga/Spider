#FROM redis:latest
FROM python:latest
# 
ENV PYTHONUNBUFFERED=1

# installing redis
RUN apt update -y && \
    apt upgrade -y && \
    apt install -y redis-server 

WORKDIR /spiderCrawler

# copying project and enrty-point file 
COPY ./DjangoWebCrawler/ ./
COPY ./entry.sh ./

# installing requirements for our project
COPY ./DjangoWebCrawler/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# exposing the container to 8000 port
EXPOSE 8000
ENTRYPOINT ["./entry.sh" ]