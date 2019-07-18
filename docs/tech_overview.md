# Tech overview 
We chose to use [Python 3](https://www.python.org/) to write the scripts.

## Downloading the files
The file is structured as a zip archive of zip archives which complicates the automatic extracting of all the files.

## The structure of the files
For each region there are 4 different files:

* **REGIONMuncipality**: All the info of the municipalities of a region, each entry contains an id and the name of the municipality in one or more languages.
* **REGIONPostalinfo**: All the info of the cities/villages of a region, each entry contains an id (the postal code) and the name of the city.
* **REGIONStreetname**: All the streetnames of a region, each entry contains an id, the status of the street (not considered in our application), the name of the street in one or more languages and a reference to the municipality id to which the street belongs.
* **REGIONAddress**: All the addresses for a region, Each entry contains an id, the position in Lambert 72 coordinates, the status of the address (not considered in our application) and references to the ids of the street, postcode and municipality to which the address belongs.

Except for Wallonia, where there is an additional file **WalloniaPartOfMuncipality**. The information contained in there does not seem to be useful so we chose to not use it.

The addresses contain the corresponding location in Lambert 72 coordinates, so using the [pyproj](http://pyproj4.github.io/pyproj/stable/) library they are converted to the WGS 84 coordinates.

## Reading XML
The original files are in saved in an XML format, especially for Flanders this gives a file of several GBs for the addresses. 
To reduce the memory load for the conversion, the XML tree is iteratively built and processed while reading the files.
This is done via the `iterparse()` function of [ElementTree](https://docs.python.org/2/library/xml.etree.elementtree.html).
The addresses are written as soon as they are fully read and afterwards the corresponding XML tree element is deleted to free up the memory.

## Filtering the files
Filtering of the files is mostly done by reading the csv file with [pandas](https://pandas.pydata.org/) and then using the DataFrame methods.
When iterating over a pandas DataFrame it is best iterate over the internal [NumPy](https://www.numpy.org/) `ndarray` which can be accessed via `DataFrame.values`.
Doing this gives us only the raw values for each row without any metadata but is much faster than the builtin `DataFrame.iterrows()`.

## Output to other formats
The resulting full csv file or the result after filtering can also be converted to several other formats:
* [GeoJSON](https://geojson.org/) (`geojson`): GeoJSON is a geospatial data interchange format based on JavaScript Object Notation (JSON). Using the [geojson](https://github.com/jazzband/python-geojson) library. The resulting geojson is a `FeatureCollection` of `Feature` containing a `Point`.
* [Shapefile](https://www.esri.com/library/whitepapers/pdfs/shapefile.pdf) (`shapefile`): A binary spatial data format. Using the [pyshp](https://pypi.org/project/pyshp/) library. To add the metadata some of the attribute names needed to be shortened as shapefiles only allow for a maximum length of 10 characters. The resulting files contain a collection of points with the corresponding metadata saved in a record.

## Matching of files
To match two different files we first need a mapping between the columns of the files. This is done via a json dictionary passed as argument to the script. Firstly we read the first address file and save it in a dictionary with as key a tuple of the columns we are matching on and value the other data of the address. The text is transformed to lowercase so we can do case-insensitive matching. The other file is then read and for each address a tuple is constructed and if we find this tuple in the dictionary we add the position in WGS 84 coordinates and the address id to the address. 