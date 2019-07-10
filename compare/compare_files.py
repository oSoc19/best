import pandas as pd
import argparse
import logging
import sys
import json


def get_best_logger(log_file, verbose):
    # Setup logger - (Python logger breaks PEP8 by default)
    logger = logging.getLogger(__name__)
    if verbose:
        logger.setLevel('DEBUG')
    # file_handler logs to file, stream_handler to console
    file_handler = logging.FileHandler(log_file)
    stream_handler = logging.StreamHandler()
    # formatter sets log format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s : %(levelname)s - %(message)s')
    # add formatter to both handlers
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    # add both handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger


def compare_addresses(args):
    """Compare the addresses of two files
    """
    logger.info('Started reading BOSA address file')
    try:
        bosa = pd.read_csv(args.input_file_1)
        logger.info('Read the BOSA address file')
    except IOError as io:
        logger.fatal(io)
        sys.exit(1)

    logger.info('Started reading comparison file')
    try:
        comparison = pd.read_csv(args.input_file_2)
        logger.info('Read the comparison file')
    except IOError as io:
        logger.fatal(io)
        sys.exit(1)


def get_city(file, city):
    return file[file['postcode'] == city]


if __name__ == "__main__":
    # Setup argument parser
    parser = argparse.ArgumentParser(
        description='Compare addresses between two csv files.')
    parser.add_argument(
        'input_file_1', help='BOSA address file, in csv format')
    parser.add_argument(
        'input_file_2', help='Address file to compare to BOSA address file, in csv format')
    parser.add_argument('output_file', help='Name of file to write output to')
    parser.add_argument('--mode', default='exact',
                        choices=['exact', 'fuzzy'], help='How to compare the addresses')
    parser.add_argument(
        '--mapping', type=json.loads, help='Column names to consider in the comparison and how they map to the \
            column names of the BOSA address file. (as a json dict of {comparison_key: bosa_key})')
    parser.add_argument('--log_name', default="compare.log",
                        help='name of the log file')
    parser.add_argument('--verbose', action="store_true",
                        help="toggle verbose output",  default=False)

    args = parser.parse_args()

    logger = get_best_logger(args.log_name, args.verbose)

    compare_addresses(args)
