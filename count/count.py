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

def count(args):
    logger.info('Started reading BOSA address file')
    try:
        bosa = pd.read_csv(args.input_file)
        logger.info('Read the BOSA address file')
    except IOError as io:
        logger.fatal(io)
        sys.exit(1)

    key = 'streetname_{}'.format(args.lang)
    result = bosa[['postcode', key]].drop_duplicates().groupby(key).count().reset_index()
    result.columns = [key, 'count']

    try:
        result.to_csv(args.output_file, index=False)
    except IOError as io:
        logger.fatal(io)
        sys.exit(1)



if __name__ == "__main__":
    # Setup argument parser
    parser = argparse.ArgumentParser(
        description='Count how many times a streetname occurs accross all muncipalities.')
    parser.add_argument(
        'input_file', help='BOSA address file, in csv format')
    parser.add_argument('output_file', help='Name of file to write output to')
    parser.add_argument('--lang', choices=['nl', 'fr', 'de'], default='nl', help='Language of the streetname')
    parser.add_argument('--log_name', default="compare.log",
                        help='name of the log file')
    parser.add_argument('--verbose', action="store_true",
                        help="toggle verbose output",  default=False)

    args = parser.parse_args()

    logger = get_best_logger(args.log_name, args.verbose)

    count(args)