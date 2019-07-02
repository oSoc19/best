import xml.etree.ElementTree as ET

paths = {
    'BrusselsAddress': '/home/theo/Downloads/bestdata/BrusselsAddress20190619/BrusselsAddress20190619L72.xml',
    'BrusselsMunicipality': '/home/theo/Downloads/bestdata/BrusselsMunicipality20190619.xml',
    'BrusselsPostalinfo': '/home/theo/Downloads/bestdata/BrusselsPostalinfo20190619.xml',
    'BrusselsStreetname': '/home/theo/Downloads/bestdata/BrusselsStreetname20190619/BrusselsStreetname20190619L72.xml',
    'FlandersAddress': '/home/theo/Downloads/bestdata/FlandersAddress20190616L72.xml',
    'FlandersMunicipality': '/home/theo/Downloads/bestdata/FlandersMunicipality20190616L72.xml',
    'FlandersPostalinfo': '/home/theo/Downloads/bestdata/FlandersPostalinfo20190616L72.xml',
    'FlandersStreetname': '/home/theo/Downloads/bestdata/FlandersStreetname20190616L72.xml',
    'WalloniaAddress': '/home/theo/Downloads/bestdata/WalloniaAddress20190610L72/WalloniaAddress20190610L72.xml',
    'WalloniaMunicipality': '/home/theo/Downloads/bestdata/WalloniaMunicipality20190610.xml',
    'WalloniaPartOfMunicipality': '/home/theo/Downloads/bestdata/WalloniaPartOfMunicipality20190610.xml',
    'WalloniaPostalinfo': '/home/theo/Downloads/bestdata/WalloniaPostalinfo20190610.xml',
    'WalloniaStreetname': '/home/theo/Downloads/bestdata/WalloniaStreetname20190610L72/WalloniaStreetname20190610L72.xml',
}


def read_xml_files(paths):
    br_munc = ET.parse(paths['BrusselsMunicipality']).getroot()
    br_street = ET.parse(paths['BrusselsStreetname']).getroot()
    br_postal = ET.parse(paths['BrusselsPostalinfo']).getroot()

    muncs = read_municipalities(br_munc)
    postal = read_postalinfos(br_postal)
    print(postal)


def read_postalinfos(element):
    postalinfos = {}
    for child in element:
        if 'PostalInfo' in child.tag:
            postalinfo = read_postalinfo(child)
            postalinfos[postalinfo['postcode']] = postalinfo
    return postalinfos


def read_postalinfo(element):
    postalinfo = {}
    for child in element:
        if 'postcode' in child.tag:
            postalinfo['postcode'] = child.findtext(
                '{http://vocab.belgif.be/ns/inspire/}objectIdentifier')
        elif 'postname' in child.tag:
            lang = child.findtext(
                '{http://vocab.belgif.be/ns/inspire/}language')
            postalinfo['postname_{}'.format(
                lang)] = child.findtext('{http://vocab.belgif.be/ns/inspire/}spelling')
    return postalinfo


def read_municipalities(element):
    municipalities = {}
    for child in element:
        if 'Municipality' in child.tag:
            municipality = read_muncipality(child)
            municipalities[municipality['municipality_id']] = municipality
    return municipalities


def read_muncipality(element):
    muncipality = {}
    for child in element:
        if 'municipalityCode' in child.tag:
            muncipality['municipality_id'] = child.findtext(
                '{http://vocab.belgif.be/ns/inspire/}objectIdentifier')
        elif 'municipalityName' in child.tag:
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
