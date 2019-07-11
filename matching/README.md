# Match addresses of secondary file to BOSA address file
This script compares the addresses of a secondary csv file to the BOSA csv file of addresses. When an address matches the address ID and coordinates are added to the resulting csv file.

## Installation
This script is written in Python 3, see the [requirements.txt](../requirements.txt) for the necessary dependencies. They can be installed by executing `pip install -r requirements.txt`.

## Usage
```
usage: matching.py [-h] [--mode {exact}] [--mapping MAPPING]
                   [--log_name LOG_NAME] [--verbose]
                   input_file_1 input_file_2 output_file

Compare addresses between two csv files.

positional arguments:
  input_file_1         BOSA address file, in csv format
  input_file_2         Address file to compare to BOSA address file, in csv
                       format
  output_file          Name of file to write output to

optional arguments:
  -h, --help           show this help message and exit
  --mode {exact}       How to compare the addresses.
  --mapping MAPPING    Column names to consider in the comparison and how they
                       map to the column names of the BOSA address file. (as a
                       json dict of {comparison_key: bosa_key})
  --log_name LOG_NAME  name of the log file
  --verbose            toggle verbose output
```
## Specifying the mapping
For the matching to work a mapping needs to be provided between the relevant columns of the BOSA address file and the columns of the secondary file. This is done by providing a json dictionary as value for the `mapping` argument. This dictionary goes from the column name of the secondary file to the column name of the BOSA file. See the [README](../converter/README.md) of the conversion script for the column names in the BOSA file and their explanation.

## Examples
Match the addresses of a secondary file to the BOSA file.
```bash
python matching.py <path to addressfile> <path to secondary file> matching.csv --mapping '{"Straat":"streetname_nl", "Huisnr":"house_number", "Postcode":"postcode"}'
```

