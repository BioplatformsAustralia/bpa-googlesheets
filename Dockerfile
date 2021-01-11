FROM python:3.8-slim
LABEL maintainer "https://github.com/bioplatformsaustralia/"

ENV VIRTUAL_ENV /env
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN addgroup --gid 1000 bioplatforms \
    && adduser --disabled-password --home /data --no-create-home --system -q --uid 1000 --ingroup bioplatforms bioplatforms \
    && mkdir /data \
    && chown bioplatforms:bioplatforms /data /env

RUN pip install --upgrade virtualenv pip

USER bioplatforms

ENV VIRTUAL_ENV /env
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# create a virtual env in $VIRTUAL_ENV and ensure it respects pip version
RUN virtualenv $VIRTUAL_ENV && $VIRTUAL_ENV/bin/pip install
ENV PIP_NO_CACHE_DIR "off"
ENV PYTHONUNBUFFERED 1

COPY . /app
WORKDIR /app
RUN pip install poetry
RUN poetry install

VOLUME /data
ENV HOME /data
WORKDIR /data