#
FROM python:3.8-slim
LABEL maintainer "https://github.com/bioplatformsaustralia/"

RUN addgroup --gid 1000 bpagooglesheets \
  && adduser --disabled-password --home /data --no-create-home --system -q --uid 1000 --ingroup bpagooglesheets bpagooglesheets \
  && mkdir /data \
  && chown bpagooglesheets:bpagooglesheets /data

ADD requirements.txt /
RUN pip install --upgrade -r /requirements.txt

VOLUME /data

USER bpagooglesheets
ENV HOME /data
WORKDIR /data