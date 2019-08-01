FROM ubuntu:18.04

RUN groupadd -r -g 1000 appuser && useradd -r -u 1000 -g appuser -m appuser
RUN apt-get update &&\
    apt-get install -y \
        git \
        python3 \
        python3-pip \
        python3-pyproj &&\
    # Switch to home directory of appuser
    cd /home/appuser &&\
    git clone https://github.com/oSoc19/best &&\
    # Go inside best repository to install requirements
    cd best &&\
    pip3 install --no-cache-dir -r requirements.txt &&\
    # After installation of the packages and the cloning of the repository, remove git and pip
    apt-get autoremove -y git python3-pip &&\
    # Make an output directory for bind mount (so the files from this container are accessible to the host machine)
    mkdir out &&\
    # Give appuser ownership of everything inside its home folder
    chown -R appuser:appuser /home/appuser
USER appuser
WORKDIR /home/appuser/best
