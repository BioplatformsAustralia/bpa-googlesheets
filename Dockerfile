#
FROM python:3.8-slim
LABEL maintainer "https://github.com/bioplatformsaustralia/"

ENV VIRTUAL_ENV /env

RUN addgroup --gid 1000 bioplatforms \
    && adduser --disabled-password --home /data --no-create-home --system -q --uid 1000 --ingroup bioplatforms bioplatforms \
    && mkdir /data \
    && chown bioplatforms:bioplatforms /data \
    && mkdir /env \
    && chown bioplatforms:bioplatforms /env
USER bioplatforms

COPY . /app
WORKDIR /app
RUN python3 -m venv $VIRTUAL_ENV \
    && . $VIRTUAL_ENV/bin/activate \
    && pip install --upgrade -r requirements.txt

VOLUME /data
ENV HOME /data

ENTRYPOINT ["/bin/sh"]