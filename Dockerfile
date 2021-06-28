FROM python:3.9-alpine
MAINTAINER TestAdmin

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client jpeg-dev zlib-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /fileshare
WORKDIR /fileshare
COPY ./fileshare /fileshare

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser -D testadmin
RUN chown -R testadmin /vol/
RUN chown -R testadmin /usr/local/lib/
RUN chown -R testadmin /fileshare/
RUN chmod -R 777 /vol/web/
USER testadmin
