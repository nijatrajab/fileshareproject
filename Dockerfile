FROM python:3.9-slim
MAINTAINER TestAdmin

COPY ./requirements.txt /requirements.txt
RUN apt-get update \
	&& apt-get install python3-opencv libpq-dev gcc -y \
	&& apt-get clean \
	&& pip install psycopg2
RUN pip install -r /requirements.txt

RUN mkdir /fileshare
WORKDIR /fileshare
COPY ./fileshare /fileshare

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser testadmin
RUN chown -R testadmin /vol/
RUN chown -R testadmin /usr/local/lib/
RUN chown -R testadmin /fileshare/
RUN chmod -R 777 /vol/web/
USER testadmin