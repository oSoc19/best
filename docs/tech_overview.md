# Tech overview 
We chose to use Python 3 to write the scripts.

## Downloading the files
The file is structured as a zip archive of zip archives which complicates the automatic extracting of all the files.

## The structure of the files
For each region there are 4 different files:
* **REGIONAddress**: All the addresses for a region
* **REGIONPostalinfo**: All the info of the cities/villages of a region
* **REGIONMuncipality**: All the info of the muncipalities of a region
* **REGIONStreetname**: All the streetnames of a region

Except for Wallonia, where there is an additional file **WalloniaPartOfMuncipality**. The information contained in there does not seem to be useful so we chose to not use it.

The addresses contain the corresponding location in Lambert 72 coordinates.

## Reading XML
The original files are in saved in an XML format especially for Flanders this gives a file of several GBs for the addresses. 
To reduce the memory load for the conversion, the XML tree is iteratively built and processed while reading the files.
This is done via the `iterparse()` function of [ElementTree](https://docs.python.org/2/library/xml.etree.elementtree.html).
The addresses are written as soon as they are fully read and afterwards the corresponding XML tree element is deleted to free up the memory.

## Filtering the files
Filtering of the files is mostly done by reading the csv file with [pandas](https://pandas.pydata.org/) and then using the DataFrame methods.
When iterating over a pandas DataFrame it is best iterate over the internal [NumPy](https://www.numpy.org/) `ndarray` which can be accessed via `DataFrame.values`.
Doing this gives us only the raw values for each row without any metadata but is much faster than the builtin `DataFrame.iterrows()`.
