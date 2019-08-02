# BeSt

Various tools to use and convert the [BeST streets and addresses open data](https://opendata.bosa.be/index.nl.html)

## Table of contents
- [BeSt](#best)
  - [Table of contents](#table-of-contents)
  - [Overview](#overview)
  - [Scripts](#scripts)
    - [Downloader](#downloader)
    - [Converter](#converter)
    - [Filter](#filter)
    - [Matching](#matching)
    - [Count](#count)
    - [Compare](#compare)
  - [Docker](#docker)
  - [Openaddresses](#openaddresses)
  - [Pelias](#pelias)
  - [Marketing](#marketing)
  - [Notebooks](#notebooks)
  - [Interactive map](#interactive-map)

## Overview

![Components overview](/docs/components.png)

## Scripts
This repository contains a collection of scripts to perform various operations with the [BeST streets and addresses open data](https://opendata.bosa.be/index.nl.html).

### Downloader
The download script downloads the dataset and unzips it in the specified directory.

View the [documentation](downloader/README.md)

### Converter
The convert script converts the xml files in the dataset to one big csv file.

View the [documentation](converter/README.md)
### Filter
The filter script can filter the csv file on postcode and bounding box and can output the result in various formats

View the [documentation](filter/README.md)
### Matching
The matching script can match the addresses of one file to the addresses of another file and will fill in the official address id and GPS coordinates

View the [documentation](matching/README.md)
### Count
The Count scripts can count the occurences of streetnames in the file

View the [documentation](count/README.md)
### Compare
The compare script compares the streetnames of two groups of postal codes and return the common ones.

View the [documentation](compare/README.md)

## Docker


## Openaddresses
Contains the metadata for our upload to the [openaddresses.io](https://openaddresses.io) global open address repository, and some more information on the process.

View the [documentation](openaddresses/README.md).

## Pelias
Contains information on how to set up a pelias geocoding service that uses the BeSt data.

View the [documentation](pelias/README.md)

## Marketing
A collection of marketing and communication assets are prepared for the promotion of the dataset and other similar datasets in the future.

They can be found [here](marketing/README.md)

## Notebooks
Using the csv data a few notebooks were created using the data in fun and interesting ways.

View the [documentation](visualizations/README.md)

## Interactive map
An interactive map visualization off all addresses in Belgium can be found [here](https://github.com/oSoc19/best/tree/master/visualizations/server)

Along with the [information](visualizations/server/README.md) on how to run it.
