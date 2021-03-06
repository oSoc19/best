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

    comp_keys = []
    bosa_ids = []
    for comp_key, bosa_key in args.mapping.items():
        try:
            comp_keys.append(comp_key)
            bosa_ids.append(bosa.columns.get_loc(bosa_key))
        except KeyError as ke:
            logger.error(
                'Column %s of column mapping (%s -> %s) not found in BOSA file', ke, comp_key, bosa_key)
            sys.exit(1)

    address_dict = {}
    logger.info('Building data structure to perform matching')
    for i, row in enumerate(bosa.values):
        if i % 50_000 == 0:
            logger.info('Processed %i / %i addresses', i, len(bosa))
        address_dict[tuple(el.lower() if type(
            el) == str else el for el in row[bosa_ids])] = row

    extended = perform_exact_matching(
        bosa, comparison, address_dict, comp_keys)

    try:
        extended.to_csv(args.output_file, index=False)
    except IOError as io:
        logger.fatal(io)
        sys.exit(1)


def perform_exact_matching(bosa, comparison, address_dict, comp_keys):
    """Match the addresses in the comparison file and add address_id and coordinates when matched
    """
    addr_id = bosa.columns.get_loc('address_id')
    lon_id = bosa.columns.get_loc('EPSG:4326_lon')
    lat_id = bosa.columns.get_loc('EPSG:4326_lat')

    extended = []
    logger.info('Performing matching')
    for i, row in comparison.iterrows():
        if i % 50_000 == 0:
            logger.info('Matched %i / %i addresses', i, len(comparison))
        try:
            key = tuple(el.lower() if type(el) ==
                        str else el for el in row[comp_keys])
        except KeyError as ke:
            logger.error('Column %s not found in the comparison file', ke)
            sys.exit(1)
        if key in address_dict:
            # If the address is matched add address_id and coordinates to it
            data = address_dict[key]
            row['address_id'] = data[addr_id]
            row['EPSG:4326_lon'] = data[lon_id]
            row['EPSG:4326_lat'] = data[lat_id]
        extended.append(row)
    extended = pd.DataFrame(extended)
    # Convert column to int type that can handle NaN
    extended['address_id'] = extended['address_id'].astype('Int64')

    return extended


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
                        choices=['exact'], help='How to compare the addresses.')
    parser.add_argument(
        '--mapping', default={}, type=json.loads, help='Column names to consider in the comparison and how they map to the \
            column names of the BOSA address file. (as a json dict of {comparison_key: bosa_key})')
    parser.add_argument('--log_name', default="compare.log",
                        help='name of the log file')
    parser.add_argument('--verbose', action="store_true",
                        help="toggle verbose output",  default=False)

    args = parser.parse_args()

    logger = get_best_logger(args.log_name, args.verbose)

    compare_addresses(args)
