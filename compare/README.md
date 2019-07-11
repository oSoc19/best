# Compare streetnames of two cities
This script compares the streetnames of two cities and outputs the common streetnames as a csv file.

## Installation
This script is written in Python 3, see the [requirements.txt](../requirements.txt) for the necessary dependencies. They can be installed by executing `pip install -r requirements.txt`.

## Usage
```
usage: compare.py [-h] [--log_name LOG_NAME] [--verbose]
                  input_file output_file city_1 city_2

Compare streetnames in cities.

positional arguments:
  input_file           input address file
  output_file          output file
  city_1               Postcode of first city
  city_2               Postcode of second city

optional arguments:
  -h, --help           show this help message and exit
  --log_name LOG_NAME  name of the log file
  --verbose            toggle verbose output
```

## Examples
Return the common streetnames between cities with postal codes 9980 and 9052
```bash
python compare.py <path to addressfile> common.csv 9980 9052
```

