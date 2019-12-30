from pandas import DataFrame
import plotly.graph_objects as go
from enum import Enum

class MapboxStyle(Enum):
    """Enum value for mapbox styles.
    """
    STAMEN_TERRAIN = "stamen-terrain"
    OPEN_STREET_MAP = "open-street-map"
    DARK = "dark"
    CARTO_POSITRON = "carto-positron"

class HeatMap:
    """Simple browser-based heat map. Uses Plotly Python API for launching the plot.
    See the [demo](https://plot.ly/python/mapbox-density-heatmaps/) and 
    [Densitymapbox docs](https://plot.ly/python/reference/#densitymapbox) online.

    Arguments:

        data {DataFrame} -- The data to be plotted

    Keyword Arguments:

        radius {int} -- The radius of plot marker on the map {Default: 10}
        style {MapboxStyle} -- Style of the map {Default: MapboxStyle.STAMEN_TERRAIN}
        access_token {str} -- Mapbox access token {Default: None}
    
    Example of usage::
        # Data has to contain Latitude and Longitude columns
        data = load_data()
        heat_map = HeatMap(data, style = MapboxStyle.OPEN_STREET_MAP)
        heat_map.show()
    """

    LAT = 'Latitude'
    LON = 'Longitude'

    def __init__(
        self,
        data: DataFrame,
        radius: int = 10,
        style: MapboxStyle = MapboxStyle.STAMEN_TERRAIN,
        access_token: str = None):

        assert self.LAT in data.columns, 'Data has to contain column {}'.format(self.LAT)
        assert self.LON in data.columns, 'Data has to contain column {}'.format(self.LON)

        if style == MapboxStyle.DARK:
            assert access_token is not None, 'Access token has to be ' + \
                                            'provided for dark mapbox tiles'

        self.data = data
        self.fig = go.Figure(
            go.Densitymapbox(
                lat = data[self.LAT],
                lon = data[self.LON],
                radius = radius
            )
        )
        self.style = style
        self.access_token = access_token

    def show(self, **kwargs):
        """Show the map in the default browser. All given keyword arguments are
        passed down to `self.fig.update_layout` call before the figure is shown.
        """

        min_lat = self.data[self.LAT].min()
        max_lat = self.data[self.LAT].max()
        min_lon = self.data[self.LON].min()
        max_lon = self.data[self.LON].max()

        avg_lat = min_lat + (max_lat - min_lat) / 2
        avg_lon = min_lon + (max_lon - min_lon) / 2
        # TODO: Is it possible to calculate the zoom properly?
        zoom = 6

        self.fig.update_layout(
            mapbox_style = self.style.value,
            mapbox_center_lat = avg_lat,
            mapbox_center_lon = avg_lon,
            mapbox_zoom = zoom,
            margin = {
                "r": 0,
                "t": 0,
                "l": 0,
                "b": 0
            },
            # Not necessarily needed
            mapbox_accesstoken = self.access_token,
            **kwargs
        )
        self.fig.show()
