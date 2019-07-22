# Setup guide for Pelias geocoding service.

This guide explains how we set up the geocoding service for https://best.osoc.be.

This folder contains configuration files to download/prepare/build a complete Pelias installation for Belgium
using the BOSA open address database and various other open data sources.
It also describes how to set up an apache webserver as a proxy and to make the service serve over [https with certbot](https://certbot.eff.org/).
This guide was adapted from https://github.com/pelias/docker/tree/master/projects/belgium .

# Why Pelias?

We chose pelias for a couple of reasons:
* It is open source.
* It offers a very useful API for forward and reverse geocoding, and even for autocompletion.
* It provides easy [openaddresses.io](https:openaddresses.io) integration. Which makes it particulary interesting for our project.
* It is well documented.
* It also offers data from other data sources, which makes it useful in all kinds of applications. It provides more than just address lookup.
* Setup with this guide should be pretty straightforward. You can get a Belgian instance of Pelias running in about an hour (depending on your computer/server specs).

Other (open source) geocoding systems that could also be used with our data, but that are not discussed here:
* [Addok](https://github.com/addok/addok) (made by French and used on https://adresse.data.gouv.fr/map)
* [Photon](https://github.com/komoot/photon)

# Setup

Please refer to the instructions at <https://github.com/pelias/docker> in order to install and configure your docker environment.

The minimum configuration required in order to run this project are [installing prerequisites](https://github.com/pelias/docker#prerequisites), [install the pelias command](https://github.com/pelias/docker#installing-the-pelias-command) and [configure the environment](https://github.com/pelias/docker#configure-environment).

Please ensure that's all working fine before continuing.

# Download BOSA data

At the time of writing, the dataset of bosa

# Run a Build

To run a complete build, execute the following commands:

```bash
pelias compose pull
pelias elastic start
pelias elastic wait
pelias elastic create
pelias download all
pelias prepare all
pelias import all
pelias compose up
```

# Make an Example Query

You can now make queries against your new Pelias build:

<http://localhost:4000/v1/search?text=Brussels>
