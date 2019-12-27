import argparse
import json

"""
A script that takes input GeoJSON file (--in arg), and filters out all features that are not
in London area. The output file can be specified as --out argument. This is strictly data-specific;
GeoJSON features are expected to contain key `PostArea` in properties. See more details from where
the data can be sourced.

Data can be sourced from https://datashare.is.ed.ac.uk/handle/10283/2597
    * Contains the whole UK postal areas, districts and sectors in shapefile format
        * Areas (AB, EH,..), districts (AB1, AB2,..) and sectors (AB1 1, AB1 2, ..)
        * Has to be converted from shapefiles to GeoJSON
        * When converted to GeoJSON
            * PostalArea contains 120 features (114,7 Mt)
            * PostalDistrict contains 2736 features (239,9 Mt)
            * PostalSector contains 9232 features (357,3 Mt)
            * See examples -directory for the shapes of features

Example usage:
python ../../geoutils/london_codes.py PostalArea.geojson --out ../geojson/london/PostalArea.geojson
"""
CODES_LONDON_AREA_INNER = [ "E", "EC", "N", "NW", "SE", "SW", "W", "WC" ]
CODES_LONDON_AREA_OUTER = [ "BR", "CR", "DA", "EN", "HA", "IG", "SL", "TN", "KT", "RM", "SM", "TW", "UB", "WD"]
CODES_LONDON_AREA_ALL = CODES_LONDON_AREA_INNER + CODES_LONDON_AREA_OUTER


parser = argparse.ArgumentParser(
    description='Filter out areas from GeoJSON file with London area post codes'
)
parser.add_argument('input', metavar='F', type=str, nargs='?', help='Path to the input GeoJSON file')
parser.add_argument(
    '--out',
    metavar='O',
    type=str,
    nargs='?',
    default='output.geojson',
    help='Path to the output GeoJSON file'
)
parser.add_argument(
    '--id',
    metavar='I',
    type=str,
    nargs='?',
    default='PostArea',
    help='The property name to pick from feature.properties and set as feature.id'
)

args = parser.parse_args()

geojson_file = args.input if args.input else None
output = args.out if args.out else None
property_id = args.id if args.id else None

if geojson_file is None:
    print("Please give proper input file as first positional argument")
    exit(1)

if output is None:
    print("Give the output file as --out argument")
    exit(1)

if property_id is None:
    print("Give id property name --id argument")
    exit(1)

with open(geojson_file) as json_file:
    geojson = json.load(json_file)

parsed = {
    'type': geojson['type'],
    'name': geojson['name']
}
features = []

for feature in geojson['features']:
    post_area = feature['properties']['PostArea']
    if post_area in CODES_LONDON_AREA_ALL:
        feature['id'] = feature['properties'][property_id]
        features.append(feature)

parsed['features'] = features

print("{} features found".format(len(features)))
print("Saving JSON to {}".format(output))

with open(output, 'w') as outfile:
    json.dump(parsed, outfile, indent=4)

print("Done")
