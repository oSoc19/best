import pandas as pd
import argparse
import logging
import sys


def filter_file(args):
    """Filter a csv file
    """
    try:
        file = pd.read_csv(args.input_file)
    except IOError as io:
        logging.fatal(io)
        sys.exit(1)

    result = file
    # select the addresses for a certain postcode
    if args.postcode:
        result = file[file['postcode'] == args.postcode]

    try:
        result.to_csv(args.output_file)
    except IOError as io:
        logging.fatal(io)
        sys.exit(1)


if __name__ == "__main__":
    # Setup argument parser
    parser = argparse.ArgumentParser(
        description='Filter an address file on postcode.')
    parser.add_argument(
        'input_file', help='input address file')
    parser.add_argument('output_file', help='output file')
    parser.add_argument('--postcode', help='postcode to filter on')

    args = parser.parse_args()
    filter_file(args)
