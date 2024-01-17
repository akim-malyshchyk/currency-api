FROM python:3.10

ENV PYTHONUNBUFFERED 1
ENV C_FORCE_ROOT true

WORKDIR /src

ADD ./src /src

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
