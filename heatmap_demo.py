import pandas as pd
import plotly.graph_objects as go
from app.file.utils import read_csv_directory
from app.map.heat_map import HeatMap

COLUMNS = [HeatMap.LAT, HeatMap.LON]
DATA_DIRECTORY = './datasets/data.police.uk/2016-11'

crimes = read_csv_directory(
    DATA_DIRECTORY,
    COLUMNS,
    30
)

print('Plotting {} data points...'.format(crimes.count()['Latitude']))

heat_map = HeatMap(crimes)
heat_map.show()

