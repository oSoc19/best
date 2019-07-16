FROM python:3.7.4-alpine

# Install git to get code, install build base to install needed libraries
RUN apk add git --no-cache &&\
    apk add build-base --no-cache &&\
    git clone https://github.com/oSoc19/best &&\    
    cd best &&\
    pip install -no-cache-dir wheel
    pip install -no-cache-dir -r requirements.txt &&\
    apk del git &&\
    apk del build-base



