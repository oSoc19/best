import pandas as pd
import argparse
import logging
import sys


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


def filter_file(args):
    """Filter a csv file
    """
    logger.info('Started reading input file')
    try:
        file = pd.read_csv(args.input_file)
        logger.info('Read input file')
    except IOError as io:
        logger.fatal(io)
        sys.exit(1)

    result = file
    # select the addresses for a certain postcode
    if args.postcode:
        logger.info('Filtering on postcode')
        result = result[result['postcode'].isin(args.postcode)]

    # Select the addresses in a bounding box
    if args.bbox:
        logger.info('Filtering on bounding box')
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
        logger.fatal(io)
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
    parser.add_argument('--postcode', nargs='*', type=int,
                        help='postcode(s) to filter on')
    parser.add_argument(
        '--bbox', type=float, nargs=4, help='Bounding box to filter on, format: min_x max_x min_y max_y (in EPSG:4326 coordinates)')
    parser.add_argument('--log_name', default="filter.log",
                        help='name of the log file')
    parser.add_argument('--verbose', action="store_true",
                        help="toggle verbose output",  default=False)

    args = parser.parse_args()

    logger = get_best_logger(args.log_name, args.verbose)

    filter_file(args)
