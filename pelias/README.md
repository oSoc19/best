# Setup guide for Pelias geocoding service.

This guide explains how we set up the geocoding service for <https://best.osoc.be>.

This folder contains configuration files to download/prepare/build a complete Pelias installation for Belgium
using the BOSA open address database and various other open data sources.
It also describes how to set up an apache webserver as a proxy and to make the service serve over https with [certbot](https://certbot.eff.org/).
This guide was adapted from <https://github.com/pelias/docker/tree/master/projects/belgium> .

# Why Pelias?

We chose pelias for a couple of reasons:
* It is open source.
* It offers a very useful API for forward and reverse geocoding, and even for autocompletion.
* It provides easy [openaddresses.io](https://openaddresses.io) integration. Which makes it particulary interesting for our project.
* It is well documented.
* It also offers data from other data sources, which makes it useful in all kinds of applications. It provides more than just address lookup.
* Setup with this guide should be pretty straightforward. You can get a Belgian instance of Pelias running in about an hour (depending on your computer/server specs).

Other (open source) geocoding systems that could also be used with our data, but that are not discussed here:
* [Addok](https://github.com/addok/addok) (made by French and used on <https://adresse.data.gouv.fr/map>)
* [Photon](https://github.com/komoot/photon)

# Setup

Please refer to the instructions at <https://github.com/pelias/docker> in order to install and configure your docker environment.

The minimum configuration required in order to run this project are [installing prerequisites](https://github.com/pelias/docker#prerequisites), [install the pelias command](https://github.com/pelias/docker#installing-the-pelias-command) and [configure the environment](https://github.com/pelias/docker#configure-environment).

Please ensure that's all working fine before continuing.

# Run a Build

Before you start you should check this:
If you setup a proxy, your attribution link in the JSON-response will be wrong.
You can set this up beforehand in the `pelias.json` file.
Set your `"attributionURL"` correctly
```json
},
  "attributionURL": {"url": "https://<yourdomain.example.com>/attribution"}
},
```
If you forgot to do this. Take a look at the useful commands section below. You can also change this setting later.

To run a complete build, execute the following commands:

```bash
pelias compose pull   # will pull all necessary docker containers
pelias elastic start  # will start the elastic search container
pelias elastic wait   # waits for the elastic server to be setup (useful for scripts)
pelias elastic create # create an instance of elastic search
pelias download all   # download all the datasets
```
The `pelias compose pull` and `pelias download all` commands can easily take up half an hour.
It depends on your network speed.

At the time of writing, the dataset of bosa was not available through <https://openaddresses.io> and thus did not get downloaded with the `pelias download all` command. A workaround is needed:
Download following files on your server, the most recent versions are listed on <http://results.openaddresses.io/?runs=all#runs> (click on `zip`):
```
https://s3.amazonaws.com/data.openaddresses.io/runs/655500/be/wal/bosa-region-wallonia-fr.zip
https://s3.amazonaws.com/data.openaddresses.io/runs/655501/be/vlg/bosa-region-flanders-nl.zip
https://s3.amazonaws.com/data.openaddresses.io/runs/655502/be/bru/bosa-region-brussels-fr.zip
https://s3.amazonaws.com/data.openaddresses.io/runs/655503/be/bru/bosa-region-brussels-nl.zip
```
This guide will expect all downloaded files to be in the `/data`-folder of your system.
All the files that you download must also be unzipped:
```bash
unzip /data/bosa-region-brussels-fr.zip
unzip /data/bosa-region-brussels-nl.zip
unzip /data/bosa-region-flanders-nl.zip
unzip /data/bosa-region-wallonia-nl.zip
```
You have to make sure the files are located as follows (location of the `.vrt`-files is not important):
```
/data/openaddresses
└── be
    ├── bru
    │   ├── bosa-region-brussels-fr.csv
    │   └── bosa-region-brussels-nl.csv
    ├── vlg
    │   └── bosa-region-flanders-nl.csv
    └── wal
        └── bosa-region-wallonia-fr.csv
```
Then you can continue setting up the service as follows.
The `prepare all` and `import all` can easily take up 30 minutes, depending on your hardware.
```bash
pelias prepare all  # build all service that require preparation
pelias import all   # import all data
pelias compose up   # start up all necessary containers
```
You can now make queries against your new Pelias build:
<http://localhost:4000/v1/search?text=Brussels>.
If you set the containers up on a server you can replace `localhost` with the server's ip-addres.

# Set up a proxy

In this step we will setup an apache proxy server:
Our server is an ubuntu server (18.04.2).

## Install and setup apache
We can install the apache server with the following commands:
```
sudo apt update
sudo apt install apache2
```
Now we have to set it up by editing the `000-default.conf`. You can use `vim` or any other text-editor:
```
vim /etc/apache2/sites-available/000-default.conf
```
Edit the file to have these lines:
```
<VirtualHost *:80>
        ServerName <yourdomain.example.com>
        ServerAdmin webmaster@localhost
        ProxyPass "/" "http://localhost:4000/"
        ProxyPassReverse "/" "http://localhost:4000"
</VirtualHost>
```
Enable the `proxy` and `proxy_http` modules with this command:
```
a2enmod proxy proxy_http
```
Restart the apache server:
```
systemctl restart apache2
```
## Enable HTTPS
We use certbot to set up HTTPS. The easiest and most up-to-date instructions can be found on <https://certbot.eff.org/instructions>.
Setting this up should take about 5 minutes.

# Useful commands

* A full list of available pelias commands is available on: <https://github.com/pelias/docker#cli-commands>
* `pelias compose ps` list all currently running docker containers. Should output something like this:
```
Name                      Command               State                        Ports                     
|---------------------------------------------------------------------------------------------------------------
pelias_api             ./bin/start                      Up       0.0.0.0:4000->4000/tcp                        
pelias_csv_importer    /bin/bash                        Exit 0                                                 
pelias_elasticsearch   /bin/bash bin/es-docker          Up       0.0.0.0:9200->9200/tcp, 0.0.0.0:9300->9300/tcp
pelias_interpolation   ./interpolate server /data ...   Up       0.0.0.0:4300->4300/tcp                        
pelias_libpostal       ./bin/wof-libpostal-server ...   Up       0.0.0.0:4400->4400/tcp                        
pelias_openaddresses   /bin/bash                        Exit 0                                                 
pelias_openstreetmap   /bin/bash                        Exit 0                                                 
pelias_pip-service     ./bin/start                      Up       0.0.0.0:4200->4200/tcp                        
pelias_placeholder     ./cmd/server.sh                  Up       0.0.0.0:4100->4100/tcp                        
pelias_polylines       /bin/bash                        Exit 0                                                 
pelias_schema          /bin/bash                        Exit 0                                                 
pelias_whosonfirst     /bin/bash                        Exit 0                                                 
```
* `docker logs pelias_api` will show you which requests happend. The `-f` option allows for a "live" follow-up on the logs.
* `docker container ps` shows the active containers and their current uptime. It should show something like this:
```
CONTAINER ID        IMAGE                         COMMAND                  CREATED             STATUS              PORTS                                            NAMES
77880654d01b        pelias/interpolation:master   "./interpolate serve…"   9 days ago          Up 9 days           0.0.0.0:4300->4300/tcp                           pelias_interpolation
4636515f8f0a        pelias/pip-service:master     "./bin/start"            9 days ago          Up 9 days           0.0.0.0:4200->4200/tcp                           pelias_pip-service
80787cb2af8e        pelias/placeholder:master     "./cmd/server.sh"        9 days ago          Up 9 days           0.0.0.0:4100->4100/tcp                           pelias_placeholder
eb63dcea5076        pelias/libpostal-service      "./bin/wof-libpostal…"   9 days ago          Up 9 days           0.0.0.0:4400->4400/tcp                           pelias_libpostal
bcbe545eba55        pelias/api:master             "./bin/start"            9 days ago          Up 17 hours         0.0.0.0:4000->4000/tcp                           pelias_api
97f950b58bca        pelias/elasticsearch:5.6.12   "/bin/bash bin/es-do…"   9 days ago          Up 9 days           0.0.0.0:9200->9200/tcp, 0.0.0.0:9300->9300/tcp   pelias_elasticsearch
```
* For some settings you can change your api settings (`pelias.json`) without restarting the entire process. It goes like this:
  * `docker stop pelias_api`
  * Do your changes in the `pelias.json` file.
  * `pelias compose up` to restart the `pelias_api` container.
