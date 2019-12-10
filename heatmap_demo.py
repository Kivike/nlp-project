import pandas as pd
import plotly.graph_objects as go
import platform
from app.file.utils import read_csv_directory

if platform.system() == 'Darwin':
    # For odd SSL cert verification issue:
    # ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1056)
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context

COLUMNS = ['Latitude', 'Longitude']
# The data is located outisde of Git repository
DATA_DIRECTORY = '../data/data.police.uk/2016-11'

crimes = read_csv_directory(
    # Data located outside of the Git repository
    DATA_DIRECTORY,
    COLUMNS,
    30
)

print('Plotting {} data points...'.format(crimes.count()['Latitude']))

fig = go.Figure(
    go.Densitymapbox(
        lat = crimes.Latitude,
        lon = crimes.Longitude,
        radius = 10
    )
)

fig.update_layout(
    mapbox_style = "stamen-terrain",
    mapbox_center_lon = -1.809,
    mapbox_center_lat = 53.257,
    mapbox_zoom = 6
)
fig.update_layout(margin = { "r": 0, "t": 0, "l": 0, "b": 0 })
fig.show()



