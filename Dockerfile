FROM python:3.7.4-alpine

RUN apk add git --no-cache &&\
    apk add build-base

