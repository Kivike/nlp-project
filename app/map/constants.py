from os import path

"""A module containing several constant values regarding the application and project.
"""

# GeoJSON Files
GJSON_LONDON_AREAS = path.join(path.dirname(__file__), 'geojson/london/PostalArea.geojson')
GJSON_LONDON_DISTRICTS = path.join(path.dirname(__file__), 'geojson/london/PostalDistrict.geojson')
GJSON_LONDON_SECTORS = path.join(path.dirname(__file__), 'geojson/london/PostalSector.geojson')

# London post code areas from https://en.wikipedia.org/wiki/London_postal_district
CODES_LONDON_AREA_INNER = [ "E", "EC", "N", "NW", "SE", "SW", "W", "WC" ]
CODES_LONDON_AREA_OUTER = [ "BR", "CR", "DA", "EN", "HA", "IG", "SL", "TN", "KT", "RM", "SM", "TW", "UB", "WD"]
CODES_LONDON_AREA_ALL = CODES_LONDON_AREA_INNER + CODES_LONDON_AREA_OUTER



