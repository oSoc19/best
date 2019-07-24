# OpenAddresses submission

[openaddresses.io](https://openaddresses.io) is a global repository for open address data.
A lot of applications use the data available from this website already:
* [pelias geocoder](https://github.com/pelias/pelias/)
* [mapbox geocoding](https://docs.mapbox.com/help/how-mapbox-works/geocoding/) service. Have a look [here](https://blog.mapbox.com/openaddresses-has-440m-points-how-can-we-tell-when-were-done-caccd4a4c16d).

## How to submit

To upload address data to [openaddresses.io](https://openaddresses.io) you have to upload metadata (examples can be found in these folders and also in [the openaddresses repository](https://github.com/openaddresses/openaddresses/tree/master/sources)).
The metadata is described in a JSON-file.
It should be constructed as described in [the OpenAddresses contribution guide](https://github.com/openaddresses/openaddresses/blob/master/CONTRIBUTING.md).
This metadata is a description of where the OpenAddresses data service can find the data and how it should process it.

The metadata has to be uploaded to github.
If you make a pull request ([like this one](https://github.com/openaddresses/openaddresses/pull/4582)) and it gets accepted, the [OpenAddresses data service](http://results.openaddresses.io/jobs) will start processing your data.
The service will then also post a nice visualization in the comments of your pull request.

## Use the OpenAddresses data

In the [pelias folder](https://github.com/osoc19/best/tree/master/pelias) of this repository we explain how you can use the openaddresses data to set up your own geocoding service for Belgium in no time.
