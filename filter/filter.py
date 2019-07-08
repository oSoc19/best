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
        result = result[result['postcode'] == args.postcode]

    # Select the addresses in a bounding box
    if args.bbox:
        result = result[
            (args.bbox[0] <= result['EPSG:4326_x']) &
            (result['EPSG:4326_x'] <= args.bbox[1]) &
            (args.bbox[2] <= result['EPSG:4326_y']) &
            (result['EPSG:4326_y'] <= args.bbox[3])
        ]

    # if we only need streetnames, drop the unnecessary attributes
    if args.output_type == 'street':
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
    parser.add_argument('--output_type', default='address', choices=[
                        'address', 'street'], help='Contents of the output, either full addresses or streetnames')
    parser.add_argument('--postcode', type=int, help='postcode to filter on')
    parser.add_argument(
        '--bbox', type=float, nargs=4, help='Bounding box to filter on, format: min_x max_x min_y max_y (in EPSG:4326 coordinates)')

    args = parser.parse_args()
    filter_file(args)
