# Downloading and extracting the BOSA archive
This counts the occurences of streetnames in the dataset.

## Installation
This script is written in Python 3, see the [requirements.txt](../requirements.txt) for the necessary dependencies. They can be installed by executing `pip install -r requirements.txt`.

## Usage
```
usage: count.py [-h] [--lang {nl,fr,de}] [--log_name LOG_NAME] [--verbose]
                input_file output_file

Count how many times a streetname occurs accross all muncipalities.

positional arguments:
  input_file           BOSA address file, in csv format
  output_file          Name of file to write output to

optional arguments:
  -h, --help           show this help message and exit
  --lang {nl,fr,de}    Language of the streetname
  --log_name LOG_NAME  name of the log file
  --verbose            toggle verbose output
```

## Examples
Count the occurrences of dutch streetnames 
```bash
python count.py <path to output directory> --lang nl
```
