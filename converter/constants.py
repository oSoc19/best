from pyproj import Transformer

# Namespaces of the xml files
NS = {
    'tns': 'http://fsb.belgium.be/mappingservices/FullDownload/v1_00',
    'com': 'http://vocab.belgif.be/ns/inspire/',
    'int': 'http://fsb.belgium.be/data/common',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    'ns2': 'http://fsb.belgium.be/data/common/error/v1_00',
    'gts': 'http://www.isotc211.org/2005/gts',
    'gml': 'http://www.opengis.net/gml/3.2',
    'gco': 'http://www.isotc211.org/2005/gco',
    'pfx0': 'http://www.opengis.net/gml/3.3/xbt',
    'gss': 'http://www.isotc211.org/2005/gss',
    'gsr': 'http://www.isotc211.org/2005/gsr',
    'gmd': 'http://www.isotc211.org/2005/gmd',
    'vc': 'http://www.w3.org/2007/XMLSchema-versioning',
    'xlink': 'http://www.w3.org/1999/xlink',
    'pfx1': 'http://www.opengis.net/gml/3.3/ce'
}

# Keys for all the different xml files
FILE_KEYS = [
    'BrusselsAddress',
    'BrusselsMunicipality',
    'BrusselsPostalinfo',
    'BrusselsStreetname',
    'FlandersAddress',
    'FlandersMunicipality',
    'FlandersPostalinfo',
    'FlandersStreetname',
    'WalloniaAddress',
    'WalloniaMunicipality',
    'WalloniaPartOfMunicipality',
    'WalloniaPostalinfo',
    'WalloniaStreetname'
]

CSV_HEADER = [
    'EPSG:31370_x',
    'EPSG:31370_y',
    'EPSG:4326_lat',
    'EPSG:4326_lon',
    'address_id',
    'box_number',
    'house_number',
    'municipality_id',
    'municipality_name_de',
    'municipality_name_fr',
    'municipality_name_nl',
    'postcode',
    'postname_fr',
    'postname_nl',
    'street_id',
    'streetname_de',
    'streetname_fr',
    'streetname_nl',
    'region_code',
    'status'
]

# Transformer for the Lambert 72 coordinates to WGS 84
TRANSFORMER = Transformer.from_crs(31370, 4326)
