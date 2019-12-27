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
python ../../geoutils/london_codes.py --in PostalArea.geojson --out ../geojson/london/PostalArea.geojson
"""
LONDON_AREA = [ "E", "EC", "N", "NW", "SE", "SW", "W", "WC" ]

parser = argparse.ArgumentParser()
parser.add_argument('--in', metavar='I', nargs='?')
parser.add_argument('--out', metavar='O', nargs='?')

args = parser.parse_args()

geojson_file = args.geojson if args.geojson else None
output = args.out if args.out else None

if geojson_file is None:
    print("Give the GeoJSON file as --in argument")
    exit(1)

if output is None:
    print("Give the output file as --out argument")
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
    if post_area in LONDON_AREA:
        features.append(feature)

parsed['features'] = features
print("{} features found".format(len(features)))
print("Saving JSON to {}".format(output))

with open(output, 'w') as outfile:
    json.dump(parsed, outfile, indent=4)

print("Done")
