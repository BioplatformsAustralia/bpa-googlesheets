FROM python:3.8-slim
LABEL maintainer "https://github.com/bioplatformsaustralia/"

ENV VIRTUAL_ENV /env
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN addgroup --gid 1000 bioplatforms \
    && adduser --disabled-password --home /data --no-create-home --system -q --uid 1000 --ingroup bioplatforms bioplatforms \
    && mkdir /data \
    && chown bioplatforms:bioplatforms /data

COPY . /app
WORKDIR /app
RUN poetry install

VOLUME /data
ENV HOME /data
WORKDIR /data