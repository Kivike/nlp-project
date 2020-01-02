from area import area
from shapely.geometry import shape, Point
import json
from app.map.constants import GJSON_LONDON_SECTORS

with open(GJSON_LONDON_SECTORS) as json_file:
    geojson = json.load(json_file)

point = Point(0.140035, 51.589112)

print('Searching for {}'.format(point))

for feature in geojson['features']:
    identifier = feature['id']
    polygon = shape(feature['geometry'])
    if polygon.contains(point):
        print('Sector {} contains the point'.format(identifier))

