import pandas as pd
import argparse
import logging
import sys
import geojson
import numpy as np
from geojson import Point, Feature, FeatureCollection
import shapefile

# Datatype mapping for shapefiles
DTYPE = {
    np.dtype('int64'): 'N',
    np.dtype('float64'): 'F',
    np.dtype('object'): 'C',
}
# Column name mapping for shapefiles as they dont allow names that are longer than 10 characters
COL_NAME = {
    'EPSG:31370_x': 'E:31370_x' ,
    'EPSG:31370_y': 'E:31370_y',
    'EPSG:4326_lat': 'E:4326_y' ,
    'EPSG:4326_lon': 'E:4326_x',
    'address_id': 'address_id',
    'box_number': 'box',
    'house_number': 'house',
    'municipality_id': 'munc_id',
    'municipality_name_de': 'munc_de',
    'municipality_name_fr': 'munc_fr',
    'municipality_name_nl': 'munc_nl',
    'postcode': 'postcode',
    'postname_fr': 'postname_fr',
    'postname_nl': 'postname_nl',
    'street_id': 'street_id',
    'streetname_de': 'street_de',
    'streetname_fr': 'street_fr',
    'streetname_nl': 'street_nl',
    'region_code': 'region_code'
}


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
        file = pd.read_csv(args.input_file, dtype='unicode')
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
            (args.bbox[0] <= result['EPSG:4326_lon']) &
            (args.bbox[1] <= result['EPSG:4326_lat']) &
            (result['EPSG:4326_lon'] <= args.bbox[2]) &
            (result['EPSG:4326_lat'] <= args.bbox[3])

        ]

    # if we only need streetnames, drop the unnecessary attributes
    if args.output_type == 'street':
        result = result.drop(
            ['EPSG:31370_x',
             'EPSG:31370_y',
             'EPSG:4326_lat',
             'EPSG:4326_lon',
             'address_id',
             'house_number',
             'box_number'
             ], axis=1).drop_duplicates()

    try:
        logger.info('Writing to output file')
        if args.output_format == 'csv':
            write_csv(result, args.output_file)
        elif args.output_format == 'geojson' and args.output_type == 'address':
            write_geojson(result, args.output_file)
        elif args.output_format == 'shapefile' and args.output_type == 'address':
            write_shapefile(result, args.output_file)
        else:
            logger.error(
                'output_type street is only supported for output_format csv')
            sys.exit(1)
    except IOError as io:
        logger.fatal(io)
        sys.exit(1)


def write_csv(file, output_file):
    file.to_csv(output_file, index=False)


def write_geojson(file, output_file):
    features = []
    for i, row in file.iterrows():
        if i % 50_000 == 0:
            logger.info('Processed %s / %s adresses', i, len(file))
        point = Point((row['EPSG:4326_lon'], row['EPSG:4326_lat']))
        properties = {key: val for key,
                      val in row.to_dict().items() if not pd.isnull(val) and 'EPSG:' not in key}
        features.append(Feature(geometry=point, properties=properties))
    collection = FeatureCollection(features)
    with open(output_file, 'w') as out:
        out.write(geojson.dumps(collection))

def write_shapefile(file, output_file):
    with shapefile.Writer(output_file) as shp:
        for col_name, dtype in file.dtypes.iteritems():
            shp.field(COL_NAME[col_name], DTYPE[dtype])
        for _, row in file.iterrows():
            shp.point(row['EPSG:4326_lon'], row['EPSG:4326_lat'])
            sanitized = [None if pd.isnull(el) else el for el in row.values]
            shp.record(*sanitized)
        

if __name__ == "__main__":
    # Setup argument parser
    parser = argparse.ArgumentParser(
        description='Filter an address file on postcode.')
    parser.add_argument(
        'input_file', help='input address file')
    parser.add_argument('output_file', help='output file')
    parser.add_argument('--output_type', default='address', choices=[
                        'address', 'street'], help='Contents of the output, either full addresses or streetnames')
    parser.add_argument('--output_format', default='csv',
                        choices=['csv', 'geojson', 'shapefile'], help='Format of the output')
    parser.add_argument('--postcode', nargs='+', type=int,
                        help='postcode(s) to filter on')
    parser.add_argument(
        '--bbox', type=float, nargs=4, help='Bounding box to filter on, format: left bottom right top (in EPSG:4326 coordinates)')
    parser.add_argument('--log_name', default="filter.log",
                        help='name of the log file')
    parser.add_argument('--verbose', action="store_true",
                        help="toggle verbose output",  default=False)

    args = parser.parse_args()

    logger = get_best_logger(args.log_name, args.verbose)

    filter_file(args)
