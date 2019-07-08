import pandas as pd
import argparse


def compare_streetnames(args):
    """Compare the streetnames of two cities and write the exact matches to the output file
    """
    # read and select the relevant cities
    file = pd.read_csv(args.input_file)
    city_1 = get_city(file, args.city_1)
    city_2 = get_city(file, args.city_2)

    keys = [column for column in file.columns if 'streetname' in column]

    # convert to sets for easy intersection
    streets_1 = set([tuple(map(str, el)) for el in city_1[keys].values])
    streets_2 = set([tuple(map(str, el)) for el in city_2[keys].values])

    # take intersection and write to output file
    out = pd.DataFrame(streets_1 & streets_2, columns=keys)
    out.to_csv(args.output_file)


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

    args = parser.parse_args()
    compare_streetnames(args)
