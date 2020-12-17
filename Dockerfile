#
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
RUN pip install --upgrade -r requirements.txt && python setup.py install

USER bioplatforms
VOLUME /data
ENV HOME /data
WORKDIR /data

ENTRYPOINT ["/bin/sh"]