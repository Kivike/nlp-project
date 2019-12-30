import argparse
from os import path
import pandas as pd
from app.map.choro_map import ChoroMap
from app.map.constants import GJSON_LONDON_DISTRICTS
from app.file.utils import get_absolute_path

"""Example:
python choromap.py --data "datasets/Hotel_reviews_NLP/Tripadvisor Review Part1.xlsx"
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

args = parser.parse_args()
filename = args.data if args.data else None

if filename is None:
    print("Please specify the file location as --data argument")
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
    
    df = df[df['ZIP'].notnull()]
    df['district'] = df.apply(lambda row: row['ZIP'].split()[0], axis=1)
    post_areas = df['district'].value_counts()


    choromap = ChoroMap(
        geojson=GJSON_LONDON_DISTRICTS,
        locations=post_areas.keys(),
        z=post_areas.values
    )

    choromap.show()
except Exception as e:
    print(str(e))
    exit(1)
