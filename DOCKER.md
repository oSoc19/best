# Docker container for BeST tools
This documentation guides you through the process of using the Dockerfile to build and later run an instance of docker with all the dependencies inside.
This is probably the easiest way to get started with the tools we provided.

There are still some issues with this Dockerfile.
Please refer to the bottom of this page to view them.

## Installation

Before you proceed, please make sure to have docker properly installed on your machine, go to the [docker installation guide](https://docs.docker.com/install/).
In this tutorial we are using **Ubuntu 18.04**.

If you're all set, clone this repo:
```bash
git clone https://github.com/osoc19/best.git
```

## Build your Docker image
Now it is almost time to build your docker image from the Dockerfile.
Before you can do this, you should check that the user and group id of your user and the Dockerfile match.
To get your user id run:
```bash
id -u
```
To get the group id, use the similar command:
```bash
id -g
```
Both of these commands should return `1000`. If this is not the case, edit the Dockerfile to match your user and group id like so:
```dockerfile
RUN addgroup  -S -g <yourgroupid> appuser
RUN adduser -S -u <youruserid> appuser appuser
```
Inside the `best/`-folder of this repository on your machine run the following command (if you don't have root access please put `sudo` in front of the command):
```bash
docker build . -t best-tools
```
This can take a while (about half an hour), since the dependencies for the python scripts have to be compiled,so maybe go and grab a :coffee:. Although there are future plans to make this process faster; see **issues** on the bottom of this page.

## Run your Docker image

After the building is finished, you can check wether your image is successfully built using the following command:
```bash
docker image ls
```
It should return something like this:
```
REPOSITORY              TAG                 IMAGE ID            CREATED             SIZE
best-tools              latest              4549ba05484a        35 minutes ago      530MB
```
Now you should make a folder to save the dataset (download/conversion/...) output outside of the container. Something like:
```bash
mkdir ~/hostfolder
```
Now you're all set up to run your docker container:
```bash
docker run -it -v ~/hostfolder:/home/appuser/best/out best-tools sh
```
If everything goes well, you will be presented with this prompt:
```
~ $
```

## Use the tools

Now you have a working docker container, in which you can download and manipulate the BeST data.
The `/home/appuser/best/out` folder (inside the container) is connected to your `~/hostfolder` (outside the container) so any commands inside the container that output data should be redirected to the `/home/appuser/best/out` folder. That way you can keep your data when you exit your docker container.

### Examples:
Download the dataset:
```bash
cd /home/appuser/best/downloader
mkdir tmp
python downloader.py /tmp
cd /tmp
mv * ../../out
```
The `mv` command will throw an error, but you can ignore this.

## Issues

* The current Dockerfile uses alpine linux as its base image. Consequently the build time is very long. This can be optimised further by using a slightly bigger minimal ubuntu image for example for which precompiled libraries exist.
* The current Dockerfile contains a lot of `RUN` statements, this does not allow for minimal image size. The reason why this is not implemented is because the dockerfile is still in development, and the multiple run statements allow for caching during build time.
