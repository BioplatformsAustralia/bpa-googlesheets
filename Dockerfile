FROM python:3.8-slim
LABEL maintainer "https://github.com/bioplatformsaustralia/"

ENV VIRTUAL_ENV /env
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN addgroup --gid 1000 bioplatforms \
    && adduser --disabled-password --home /data --no-create-home --system -q --uid 1000 --ingroup bioplatforms bioplatforms \
    && mkdir /data /env \
    && chown bioplatforms:bioplatforms /data /env

RUN pip install --upgrade pip

USER bioplatforms

ENV VIRTUAL_ENV /env
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PIP_NO_CACHE_DIR "off"
ENV PYTHONUNBUFFERED 1
RUN python -m venv $VIRTUAL_ENV

COPY . /app
WORKDIR /app
RUN pip install poetry
RUN poetry install

VOLUME /data
ENV HOME /data
WORKDIR /data