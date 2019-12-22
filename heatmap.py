import argparse
from os import path
import pandas as pd
from app.map.heat_map import HeatMap
from app.file.utils import get_absolute_path

"""
Example:
python heatmap.py --crime-data datasets/2019-09-metropolitan-street.csv
"""

# TODO: Provide two datasets, and render them both with different colors?
parser = argparse.ArgumentParser()
parser.add_argument('--crime-data', metavar='C', nargs='?')
parser.add_argument('--hotel-data', metavar='H', nargs='?')

args = parser.parse_args()
filename = args.hotel_data if args.hotel_data else args.crime_data

try:
    assert filename, 'Please specify either --crime-data or --hotel-data argument'
    filepath = get_absolute_path(filename)

    assert filepath.endswith('.csv') or filepath.endswith('.xlsx'), 'The given file has to end ' + \
                                                                    'in either .csv or .xlsx'
    assert path.isfile(filepath), 'The given file {} cannot be found'.format(filepath)

    if filepath.endswith('.csv'):
        data = pd.read_csv(filepath)
    else:
        data = pd.read_excel(filepath)

    # Assertion errors regarding data e.g. Latitude and Longitude columns
    heatmap = HeatMap(data)
    heatmap.show()
except Exception as e:
    print(str(e))
    exit(1)
