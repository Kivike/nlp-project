import argparse
from os import path
import pandas as pd
from app.map.choro_map import ChoroMap
from app.map.constants import GJSON_LONDON_SECTORS
from app.file.utils import get_absolute_path

"""Example:
python choromap.py --data datasets/final_data_avg.csv --feature sentiment_crime
"""


# TODO: Provide two datasets, and render them both with different colors?
parser = argparse.ArgumentParser(
    description='Render a choropleth map using Plotly and provided postal code data of London area'
)
parser.add_argument(
    '--data',
    metavar='D',
    nargs='?',
    help='Path to the xlsx or csv file containing data with ZIP column'
)

parser.add_argument(
    '--feature',
    metavar='F',
    nargs='?',
    help='Feature to use for "magnitude" of the area'
)

parser.add_argument(
    '--area-column',
    metavar='AC',
    nargs='?',
    help='Data column name for the areas, e.g. "sector"',
    default='sector'
)

args = parser.parse_args()
filename = args.data if args.data else None
feature = args.feature if args.feature else None
area_column = args.area_column

if filename is None:
    print("Please specify the file location as --data argument")
    exit(1)
if feature is None:
    print("Please specify the feature for magnitude as --feature argument")
    exit(1)


try:
    filepath = get_absolute_path(filename)
    assert filepath.endswith('.csv') or filepath.endswith('.xlsx'), 'The given file has to end ' + \
                                                                    'in either .csv or .xlsx'

    assert path.isfile(filepath), 'The given file {} cannot be found'.format(filepath)

    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)
    
    areas = df[area_column]
    z = df[feature]

    choromap = ChoroMap(
        geojson=GJSON_LONDON_SECTORS,
        locations=areas,
        z=z
    )

    choromap.show()
except Exception as e:
    print(str(e))
    exit(1)
