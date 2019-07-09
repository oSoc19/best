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


def compare_streetnames(args):
    """Compare the streetnames of two cities and write the exact matches to the output file
    """
    logger.info('Started reading input file')
    try:
        file = pd.read_csv(args.input_file)
        logger.info('Read the input file')
    except IOError as io:
        logger.fatal(io)
        sys.exit(1)
    # select the relevant cities
    city_1 = get_city(file, args.city_1)
    city_2 = get_city(file, args.city_2)

    keys = [column for column in file.columns if 'streetname' in column]

    # convert to sets for easy intersection
    streets_1 = set([tuple(map(str, el)) for el in city_1[keys].values])
    streets_2 = set([tuple(map(str, el)) for el in city_2[keys].values])

    try:
        # take intersection and write to output file
        out = pd.DataFrame(streets_1 & streets_2, columns=keys)
        logger.info('Found %s common streetnames', len(out))
        out.to_csv(args.output_file, index=False)
    except IOError as io:
        logger.fatal(io)
        sys.exit(1)


def get_city(file, city):
    return file[file['postcode'] == city]


if __name__ == "__main__":
    # Setup argument parser
    parser = argparse.ArgumentParser(
        description='Compare streetnames in cities.')
    parser.add_argument(
        'input_file', help='input address file')
    parser.add_argument('output_file', help='output file')
    parser.add_argument('city_1', type=int, help='Postcode of first city')
    parser.add_argument('city_2', type=int, help='Postcode of second city')
    parser.add_argument('--log_name', default="compare.log",
                        help='name of the log file')
    parser.add_argument('--verbose', action="store_true",
                        help="toggle verbose output",  default=False)

    args = parser.parse_args()

    logger = get_best_logger(args.log_name, args.verbose)

    compare_streetnames(args)
