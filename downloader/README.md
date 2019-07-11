# Downloading and extracting the BOSA archive
This script downloads the BOSA archive from a url and extracts it into a directory.

## Installation
This script is written in Python 3, see the [requirements.txt](../requirements.txt) for the necessary dependencies. They can be installed by executing `pip install -r requirements.txt`.

## Usage
```
usage: downloader.py [-h] [--url URL] [--file_name FILE_NAME]
                     [--log_name LOG_NAME] [--verbose] [--no_download]
                     [--force]
                     output_dir

Download and unzip the BeST-dataset

positional arguments:
  output_dir            location to store the xml-files

optional arguments:
  -h, --help            show this help message and exit
  --url URL             url to download location of dataset
  --file_name FILE_NAME
                        use this option to change the file name
  --log_name LOG_NAME   use this option to change the log file name
  --verbose             toggle verbose output
  --no_download         Don't download file, only extract
  --force               Clean up files in output directory if it (still)
                        contains files
```

## Examples
Download and extract the dataset
```bash
python downloader.py <path to output directory> --url https://opendata.bosa.be/download/best/best-full-latest.zip
```

Only extract and cleanup output directory.
```bash
python downloader.py <path to output directory> --file_name dataset.zip --no_download --force
```