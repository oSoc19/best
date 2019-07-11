# Converting XML files to csv
This script converts the raw xml files of the BOSA archive to a csv file containing the addresses of a region.

## Installation
This script is written in Python 3, see the [requirements.txt](../requirements.txt) for the necessary dependencies. They can be installed by executing `pip install -r requirements.txt`.

## Usage
```
usage: converter.py [-h] [--log_name LOG_NAME]
                    [--region {belgium,brussels,flanders,wallonia}]
                    [--verbose]
                    input_dir output_file

Convert address XML files to other formats.

positional arguments:
  input_dir             input directory of the xml files
  output_file           output file

optional arguments:
  -h, --help            show this help message and exit
  --log_name LOG_NAME   name of the log file
  --region {belgium,brussels,flanders,wallonia}
                        region to consider
  --verbose             toggle verbose output
```

## Output
The script can output all the addresses of Belgium or of a region in Belgium (Brussels, Flanders, Wallonia)

The output csv file has the following columns:
* **EPSG:31370_lat**: Latitude of address in the Lambert 72 coordinate system
* **EPSG:31370_lon**: Longitude of address in the Lambert 72 coordinate system
* **EPSG:4326_lat**: Latitude of address in the WGS 84 coordinate system
* **EPSG:4326_lon**: Longitude of address in the WGS 84 coordinate system
* **address_id**: BOSA address ID
* **box_number**: The box number of the address
* **house_number**: The house number of the address
* **municipality_id**: BOSA municipality ID
* **municipality_name_de**: The name of the municipality in German
* **municipality_name_fr**: The name of the municipality in French
* **municipality_name_nl**: The name of the municipaltiy in Dutch
* **postcode**: The postalcode of the address
* **postname_fr**: The name of the village/city in French
* **postname_nl**: The name of the village/city in Dutch
* **street_id**: BOSA street ID
* **streetname_de**: The name of the street in German
* **streetname_fr**: The name of the street in French
* **streetname_nl**: The name of the street in Dutch
* **region_code**: The ISO region code of the region in which the address is located (BE-VLG, BE-BRU or BE-WAL)


## Examples
Converting the XML files for all addresses in Belgium.
```bash
python converter.py <directory of xml files> belgium_addresses.csv 
```

Converting the XML files for the Brussels region.
```bash
python converter.py <directory of xml files> brussels_addresses.csv --region brussels
```