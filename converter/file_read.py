import xml.etree.ElementTree as ET
import pandas as pd
import logging
import argparse
import os
import sys
import re

from constants import *


def converter(args):
    """Main entry point of the application
    """
    # create a dictionary of all paths to the files
    paths = find_xml_files(args.input_dir)
    # read the addresses from the files
    addresses = read_xml_files(args.region, paths)
    # write to csv
    write_to_csv(addresses, args.region, args.output_dir)


def find_xml_files(input_dir):
    """Find all the xml files in the given directory
    """
    keys = FILE_KEYS
    paths = {}
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.split('.')[-1] == 'xml':
                m = re.search('^(.+?)[0-9]', file)
                if m:
                    key = m.group(1)
                else:
                    logging.warn(
                        'The contents of file %s can not be read by this script', file)
                if key in keys:
                    keys.remove(key)
                    paths[key] = os.path.join(root, file)
                else:
                    logging.warn(
                        'The contents of file %s can not be read by this script', file)
    if keys:
        logging.error(
            'File for data of type %s was not found in the input folder', keys)
        sys.exit(1)
    return paths


def read_xml_files(region, paths):
    """Read all XML files for the specified region
    """
    logging.info('Started reading XML files')

    addresses = []

    if region in ['belgium', 'brussels']:
        br_addresses = read_region(
            ET.parse(paths['BrusselsMunicipality']).getroot(),
            ET.parse(paths['BrusselsPostalinfo']).getroot(),
            ET.parse(paths['BrusselsStreetname']).getroot(),
            ET.iterparse(paths['BrusselsAddress'])
        )
        logging.info('Read the Brussels addresses')
        addresses += br_addresses

    if region in ['belgium', 'flanders']:
        vl_addresses = read_region(
            ET.parse(paths['FlandersMunicipality']).getroot(),
            ET.parse(paths['FlandersPostalinfo']).getroot(),
            ET.parse(paths['FlandersStreetname']).getroot(),
            ET.iterparse(paths['FlandersAddress'])
        )
        logging.info('Read the Flanders addresses')
        addresses += vl_addresses

    if region in ['belgium', 'wallonia']:
        wa_addresses = read_region(
            ET.parse(paths['WalloniaMunicipality']).getroot(),
            ET.parse(paths['WalloniaPostalinfo']).getroot(),
            ET.parse(paths['WalloniaStreetname']).getroot(),
            ET.iterparse(paths['WalloniaAddress'])
        )
        logging.info('Read the Wallonia addresses')
        addresses += wa_addresses

    return addresses


def write_to_csv(addresses, region, output_dir):
    """Write addresses to csv in the output directory
    """
    # convert to pandas dataframe for easy csv writing
    addresses_df = pd.DataFrame(addresses)
    addresses_df.to_csv(os.path.join(output_dir, '%s_addresses.csv' % region))


def read_region(muncipality_root, postalcode_root, streetname_root, address_iter):
    """Read the XML files for a region
    """
    municipalities = read_municipalities(muncipality_root)
    postalcodes = read_postalinfos(postalcode_root)
    streetnames = read_streetnames(streetname_root)

    return read_addresses(address_iter, municipalities, postalcodes, streetnames)


def read_addresses(addresses, municipalities, postcodes, streetnames):
    add_list = []
    for _, element in addresses:
        if 'Address' == element.tag.split('}')[-1]:
            address = read_address(element)
            address_join(address, municipalities, postcodes, streetnames)
            add_list.append(address)
            element.clear()

    return add_list


def address_join(address, municipalities, postcodes, streetnames):
    if 'street_id' in address:
        for key, val in streetnames[address['street_id']].items():
            address[key] = val
    else:
        logging.warn('No street id was included address %s',
                     address['address_id'])
    if 'municipality_id' in address:
        for key, val in municipalities[address['municipality_id']].items():
            address[key] = val
    else:
        logging.warn('No muncipality was included for address %s',
                     address['address_id'])
    if 'postcode' in address:
        for key, val in postcodes[address['postcode']].items():
            address[key] = val
    else:
        logging.warn('No postcode was included for address %s',
                     address['address_id'])


def read_address(element):
    address = {}
    for child in element:
        if 'addressCode' == child.tag.split('}')[-1]:
            address['address_id'] = child.findtext(
                'com:objectIdentifier', namespaces=NS)
        elif 'addressPosition' == child.tag.split('}')[-1]:
            address['pos'] = child.findtext(
                'com:pointGeometry/gml:Point/gml:pos', namespaces=NS)
        elif 'houseNumber' == child.tag.split('}')[-1]:
            address['house_number'] = child.text
        elif 'boxNumber' == child.tag.split('}')[-1]:
            address['box_number'] = child.text
        elif 'hasStreetname' == child.tag.split('}')[-1]:
            address['street_id'] = child.findtext(
                'com:Streetname/com:objectIdentifier', namespaces=NS)
        elif 'hasMunicipality' == child.tag.split('}')[-1]:
            address['municipality_id'] = child.findtext(
                'com:Municipality/com:objectIdentifier', namespaces=NS)
        elif 'hasPostalInfo' == child.tag.split('}')[-1]:
            address['postcode'] = child.findtext(
                'com:PostalInfo/com:objectIdentifier', namespaces=NS)
    return address


def read_streetnames(element):
    streetnames = {}
    for child in element:
        if 'Streetname' == child.tag.split('}')[-1]:
            streetname = read_streetname(child)
            streetnames[streetname['street_id']] = streetname
    return streetnames


def read_streetname(element):
    streetname = {}
    for child in element:
        if 'streetnameCode' == child.tag.split('}')[-1]:
            streetname['street_id'] = child.findtext(
                'com:objectIdentifier', namespaces=NS)
        elif 'streetname' == child.tag.split('}')[-1]:
            lang = child.findtext(
                'com:language', namespaces=NS)
            streetname['streetname_{}'.format(
                lang)] = child.findtext('com:spelling', namespaces=NS)
    return streetname


def read_postalinfos(element):
    postalinfos = {}
    for child in element:
        if 'PostalInfo' == child.tag.split('}')[-1]:
            postalinfo = read_postalinfo(child)
            postalinfos[postalinfo['postcode']] = postalinfo
    return postalinfos


def read_postalinfo(element):
    postalinfo = {}
    for child in element:
        if 'postcode' == child.tag.split('}')[-1]:
            postalinfo['postcode'] = child.findtext(
                'com:objectIdentifier', namespaces=NS)
        elif 'postname' == child.tag.split('}')[-1]:
            lang = child.findtext(
                'com:language', namespaces=NS)
            postalinfo['postname_{}'.format(
                lang)] = child.findtext('com:spelling', namespaces=NS)
    return postalinfo


def read_municipalities(element):
    municipalities = {}
    for child in element:
        if 'Municipality' == child.tag.split('}')[-1]:
            municipality = read_muncipality(child)
            municipalities[municipality['municipality_id']] = municipality
    return municipalities


def read_muncipality(element):
    muncipality = {}
    for child in element:
        if 'municipalityCode' == child.tag.split('}')[-1]:
            muncipality['municipality_id'] = child.findtext(
                'com:objectIdentifier', namespaces=NS)
        elif 'municipalityName' == child.tag.split('}')[-1]:
            lang = child.findtext(
                'com:language', namespaces=NS)
            muncipality['municipality_name_{}'.format(
                lang)] = child.findtext('com:spelling', namespaces=NS)
    return muncipality


if __name__ == "__main__":
    # Setup argument parser
    parser = argparse.ArgumentParser(
        description='Convert address XML files to other formats.')
    parser.add_argument(
        'input_dir', help='input directory of the xml files')
    parser.add_argument('output_dir', help='output directory')
    parser.add_argument('--log_dir', help='directory to write log files to')
    parser.add_argument('--region', help='region to consider', default='belgium',
                        choices=['belgium', 'brussels', 'flanders', 'wallonia'])

    args = parser.parse_args()
    converter(args)
