# Filtering files
Script to filter the BOSA address csv files and/or convert them to other formats.

## Installation
This script is written in Python 3, see the [requirements.txt](../requirements.txt) for the necessary dependencies. They can be installed by executing `pip install -r requirements.txt`.

## Usage
```
usage: filter.py [-h] [--output_type {address,street}]
                 [--output_format {csv,geojson}]
                 [--postcode POSTCODE [POSTCODE ...]]
                 [--bbox BBOX BBOX BBOX BBOX] [--log_name LOG_NAME]
                 [--verbose]
                 input_file output_file

Filter an address file on postcode.

positional arguments:
  input_file            input address file
  output_file           output file

optional arguments:
  -h, --help            show this help message and exit
  --output_type {address,street}
                        Contents of the output, either full addresses or
                        streetnames
  --output_format {csv,geojson}
                        Format of the output
  --postcode POSTCODE [POSTCODE ...]
                        postcode(s) to filter on
  --bbox BBOX BBOX BBOX BBOX
                        Bounding box to filter on, format: left bottom right
                        top (in EPSG:4326 coordinates)
  --log_name LOG_NAME   name of the log file
  --verbose             toggle verbose output
```
## Output
The script can output the full addresses or only the streetnames. When outputting streetnames coordinates and address data are stripped from the result.
## Filtering
### Filter on postcode
Using the `--postcode` argument multiple postcodes can be specified to be included in the result.

### Filter on region
Using the `--bbox` argument a bounding box can be specified. For this box the left, bottom, right and top boundary are specified respectively seperated by spaces. The values should be in [EPSG:4326](https://epsg.io/4326) coordinate system.


## Conversion
By default the output file is a csv file, but other formats can be specified. Supported formats are:
* [GeoJSON](https://geojson.org/) (`geojson`): GeoJSON is a geospatial data interchange format based on JavaScript Object Notation (JSON).
