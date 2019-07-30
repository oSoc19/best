FROM ubuntu:18.04

# Add new user to new group, with same gid and uid as host user
#RUN addgroup  -S -g 1000 appuser
#RUN adduser -S -u 1000 appuser appuser
    # Install git to get code, install build base to install needed libraries
RUN apt update &&\
    apt install -y \
        git \
        python3 \
        python3-pip \
        python3-pyproj &&\
    git clone https://github.com/oSoc19/best &&\
    cd best &&\
    pip3 install --no-cache-dir -r requirements.txt &&\
    apt autoremove -y git python3-pip
# Maybe it is useful to implement these commands later, to make the final image smaller.
# Note: All the RUN commands in this dockerfile should be merged into one command (RUN command_1 && command_2 ...) ,
# otherwise an extra layer is created that marks the file removal, instead of actually removing these parts of the image.
#    apk del git &&\
#    apk del build-base
# Make an output directory for bind mount (so the files from this container are accessible to the host machine)
#RUN mkdir out
#RUN chown -R appuser:appuser /home/appuser
#USER appuser
#WORKDIR /home/appuser
