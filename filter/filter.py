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

    if args.out_fmt == 'street':
        result = result.drop(
            ['EPSG:31370_x',
             'EPSG:31370_y',
             'EPSG:4326_x',
             'EPSG:4326_y',
             'address_id',
             'house_number',
             'box_number'
             ], axis=1).drop_duplicates()

    try:
        result.to_csv(args.output_file, index=False)
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
    parser.add_argument('--out_fmt', default='address', choices=[
                        'address', 'street'], help='Contents of the output, either full addresses or streetnames')
    parser.add_argument('--postcode', type=int, help='postcode to filter on')
    parser.add_argument('--bbox', help='bounding box')

    args = parser.parse_args()
    filter_file(args)
