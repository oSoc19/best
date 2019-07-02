import xml.etree.ElementTree as ET
import pandas as pd

# Temporary file dictionary
paths = {
    'BrusselsAddress': '/home/theo/Downloads/bestdata/BrusselsAddress20190619/BrusselsAddress20190619L72.xml',
    'BrusselsMunicipality': '/home/theo/Downloads/bestdata/BrusselsMunicipality20190619.xml',
    'BrusselsPostalinfo': '/home/theo/Downloads/bestdata/BrusselsPostalinfo20190619.xml',
    'BrusselsStreetname': '/home/theo/Downloads/bestdata/BrusselsStreetname20190619/BrusselsStreetname20190619L72.xml',
    'FlandersAddress': '/home/theo/Downloads/bestdata/FlandersAddress20190616L72.xml',
    'FlandersMunicipality': '/home/theo/Downloads/bestdata/FlandersMunicipality20190616L72.xml',
    'FlandersPostalinfo': '/home/theo/Downloads/bestdata/FlandersPostalinfo20190616L72.xml',
    'FlandersStreetname': '/home/theo/Downloads/bestdata/FlandersStreetname20190616L72.xml',
    'WalloniaAddress': '/home/theo/Downloads/bestdata/WalloniaAddress20190610L72/WalloniaAddress20190610.xml',
    'WalloniaMunicipality': '/home/theo/Downloads/bestdata/WalloniaMunicipality20190610.xml',
    'WalloniaPartOfMunicipality': '/home/theo/Downloads/bestdata/WalloniaPartOfMunicipality20190610.xml',
    'WalloniaPostalinfo': '/home/theo/Downloads/bestdata/WalloniaPostalinfo20190610.xml',
    'WalloniaStreetname': '/home/theo/Downloads/bestdata/WalloniaStreetname20190610L72/WalloniaStreetname20190610.xml',
}


def read_xml_files(paths):
    br_addresses = read_region_to_table(
        ET.parse(paths['BrusselsMunicipality']).getroot(),
        ET.parse(paths['BrusselsPostalinfo']).getroot(),
        ET.parse(paths['BrusselsStreetname']).getroot(),
        ET.iterparse(paths['BrusselsAddress'])
    )

    vl_addresses = read_region_to_table(
        ET.parse(paths['FlandersMunicipality']).getroot(),
        ET.parse(paths['FlandersPostalinfo']).getroot(),
        ET.parse(paths['FlandersStreetname']).getroot(),
        ET.iterparse(paths['FlandersAddress'])
    )

    wa_addresses = read_region_to_table(
        ET.parse(paths['WalloniaMunicipality']).getroot(),
        ET.parse(paths['WalloniaPostalinfo']).getroot(),
        ET.parse(paths['WalloniaStreetname']).getroot(),
        ET.iterparse(paths['WalloniaAddress'])
    )

    addresses = pd.concat([br_addresses, vl_addresses, wa_addresses], axis=1)
    addresses.to_csv('full.csv')


def read_region_to_table(muncipality_root, postalcode_root, streetname_root, address_iter):
    municipalities = read_municipalities(muncipality_root)
    postalcodes = read_postalinfos(postalcode_root)
    streetnames = read_streetnames(streetname_root)

    return read_address_table(address_iter, municipalities, postalcodes, streetnames)


def read_address_table(addresses, municipalities, postcodes, streetnames):
    add_list = []
    for _, element in addresses:
        if 'Address' == element.tag.split('}')[-1]:
            address = read_address(element)
            address_join(address, municipalities, postcodes, streetnames)
            add_list.append(address)
            element.clear()
    df = pd.DataFrame(add_list)
    return df


def address_join(address, municipalities, postcodes, streetnames):
    if 'street_id' in address:
        for key, val in streetnames[address['street_id']].items():
            address[key] = val
    if 'municipality_id' in address:
        for key, val in municipalities[address['municipality_id']].items():
            address[key] = val
    if 'postcode' in address:
        for key, val in postcodes[address['postcode']].items():
            address[key] = val


def read_address(element):
    address = {}
    for child in element:
        if 'addressCode' == child.tag.split('}')[-1]:
            address['address_id'] = child.findtext(
                '{http://vocab.belgif.be/ns/inspire/}objectIdentifier')
        elif 'addressPosition' == child.tag.split('}')[-1]:
            address['pos'] = child.findtext(
                '{http://vocab.belgif.be/ns/inspire/}pointGeometry/{http://www.opengis.net/gml/3.2}Point/{http://www.opengis.net/gml/3.2}pos')
        elif 'houseNumber' == child.tag.split('}')[-1]:
            address['house_number'] = child.text
        elif 'hasStreetname' == child.tag.split('}')[-1]:
            address['street_id'] = child.findtext(
                '{http://vocab.belgif.be/ns/inspire/}Streetname/{http://vocab.belgif.be/ns/inspire/}objectIdentifier')
        elif 'hasMunicipality' == child.tag.split('}')[-1]:
            address['municipality_id'] = child.findtext(
                '{http://vocab.belgif.be/ns/inspire/}Municipality/{http://vocab.belgif.be/ns/inspire/}objectIdentifier')
        elif 'hasPostalInfo' == child.tag.split('}')[-1]:
            address['postcode'] = child.findtext(
                '{http://vocab.belgif.be/ns/inspire/}PostalInfo/{http://vocab.belgif.be/ns/inspire/}objectIdentifier')
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
                '{http://vocab.belgif.be/ns/inspire/}objectIdentifier')
        elif 'streetname' == child.tag.split('}')[-1]:
            lang = child.findtext(
                '{http://vocab.belgif.be/ns/inspire/}language')
            streetname['streetname_{}'.format(
                lang)] = child.findtext('{http://vocab.belgif.be/ns/inspire/}spelling')
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
                '{http://vocab.belgif.be/ns/inspire/}objectIdentifier')
        elif 'postname' == child.tag.split('}')[-1]:
            lang = child.findtext(
                '{http://vocab.belgif.be/ns/inspire/}language')
            postalinfo['postname_{}'.format(
                lang)] = child.findtext('{http://vocab.belgif.be/ns/inspire/}spelling')
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
                '{http://vocab.belgif.be/ns/inspire/}objectIdentifier')
        elif 'municipalityName' == child.tag.split('}')[-1]:
            lang = child.findtext(
                '{http://vocab.belgif.be/ns/inspire/}language')
            muncipality['municipality_name_{}'.format(
                lang)] = child.findtext('{http://vocab.belgif.be/ns/inspire/}spelling')
    return muncipality


def print_structure(root):
    structure = get_structure(root)
    print_structure_part(structure, 0)


def print_structure_part(structure, level):
    for key, val in structure.items():
        print('\t' * level, key)
        print_structure_part(val, level + 1)


def get_structure(root):
    structure = {}
    for child in root:
        if child.tag not in structure:
            structure[child.tag] = get_structure(child)
    return structure


read_xml_files(paths)
