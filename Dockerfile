FROM  python:3.10.8-slim
LABEL maintainer="alexeylubchenko75@gmail.com"

WORKDIR /app


ENV PYTHONUNBUFFERED 1


RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


COPY . .

RUN apt-get update && apt-get install -y libpq-dev
