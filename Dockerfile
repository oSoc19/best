FROM python:3.7.4-alpine

# Install git to get code, install build base to install needed libraries
RUN apk add git --no-cache &&\
    # Packages necessary for building C code from python (numpy, pandas, ...)
    apk add build-base --no-cache &&\
    # Packages necessary for pyproj (from the testing repository)
    apk add proj proj-util proj-dev --repository=http://dl-3.alpinelinux.org/alpine/edge/testing/ --no-cache &&\
    git clone https://github.com/oSoc19/best &&\    
    cd best &&\
    pip install --no-cache-dir -r requirements.txt &&\
    apk del git &&\
    apk del build-base



