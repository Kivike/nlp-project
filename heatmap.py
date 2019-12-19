import argparse
from app.map.heat_map import HeatMap

"""
Example:
python heatmap.py --crime-data datasets/2019-09-metropolitan-street.csv
"""

parser = argparse.ArgumentParser()
parser.add_argument('--crime-data', metavar='C', nargs='?')
parser.add_argument('--hotel-data', metavar='H', nargs='?')

args = parser.parse_args()

print("not yet implemented")

if args.hotel_data:
    #TODO: Draw hotel heatmap from file args.hotel_data
    pass

if args.crime_data:
    #TODO: Draw crime heatmap from file args.crime_data
    pass
