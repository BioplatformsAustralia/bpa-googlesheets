#!/bin/bash

set -e


docker build -t bioplatformsaustralia/bpagooglesheets:latest .
docker push bioplatformsaustralia/bpagooglesheets
if [ x"$TRAVIS_TAG" != x"" ]; then
  docker tag bioplatformsaustralia/bpagooglesheets:latest bioplatformsaustralia/bpagooglesheets:${TRAVIS_TAG}
  docker push bioplatformsaustralia/bpagooglesheets:${TRAVIS_TAG}
fi
