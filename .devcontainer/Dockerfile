# Using the official solc alpine image from ethereum org
FROM ethereum/solc:stable-alpine

# Installing Python3 with pip
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

# Installing JDK 11
RUN apk add --no-cache openjdk11

# Installing gcc and other build apps
RUN apk add --no-cache build-base

# Installing certora python pacakge
RUN pip install certora-cli

# Changing the entrypoint from solc to certoraRun app
ENTRYPOINT ["certoraRun"]