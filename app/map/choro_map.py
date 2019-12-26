from pandas import DataFrame
import plotly.graph_objects as go
from enum import Enum
from app.map.heat_map import MapboxStyle
from typing import List

class ChoroMap:
    """Simple browser-based choropleth map. Uses Plotly Python API for launching the plot.
    See the [demo](https://plot.ly/python/mapbox-county-choropleth/).

    Arguments:

        geojson -- The geojson data respective to location and z parameters

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

    def __init__(
        self,
        geojson,
        locations: List[str] = None,
        z: List[float] = None,
        style: MapboxStyle = MapboxStyle.CARTO_POSITRON,
        access_token: str = None):

        assert locations is not None, 'Please provide the list of locations'
        assert z is not None, 'Please provide the list of z-values'
        if style == MapboxStyle.DARK:
            assert access_token is not None, 'Access token has to be ' + \
                                            'provided for dark mapbox tiles'

        self.geojson = geojson
        self.fig = go.Figure(
            go.Choroplethmapbox(
                geojson=geojson,
                locations=locations,
                z=z,
                colorscale="Viridis",
                zmin=min(z),
                zmax=max(z)
            )
        )
        self.style = style
        self.access_token = access_token

    def show(self, **kwargs):
        """Show the map in the default browser. All given keyword arguments are
        passed down to `self.fig.update_layout` call before the figure is shown.
        """

        # TODO: Is it possible to calculate the zoom properly?
        zoom = 6

        self.fig.update_layout(
            mapbox_style = self.style.value,
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
