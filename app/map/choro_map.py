from pandas import DataFrame
import json
import plotly.graph_objects as go
from enum import Enum
from app.map.heat_map import MapboxStyle
from app.map.constants import GJSON_LONDON_AREAS, CODES_LONDON_AREA_ALL
from typing import List, Union


class ChoroMap:
    """Simple browser-based choropleth map. Uses Plotly Python API for launching the plot.
    See the [demo](https://plot.ly/python/mapbox-county-choropleth/).

    Keyword Arguments:

        geojson {str} -- File path to the GeoJSON data {Default: GJSON_LONDON_AREAS}
        locations {List[str]} -- The list of locations to be drawn to the map {Default: CODES_LONDON_AREA_ALL}
        z {List[float]} -- The z-values for each location
        style {MapboxStyle} -- Style of the map {Default: MapboxStyle.STAMEN_TERRAIN}
        access_token {str} -- Mapbox access token {Default: None}
        colorscale {str} -- Colorscale, see https://plot.ly/python/builtin-colorscales/

    """

    def __init__(
        self,
        geojson: str = GJSON_LONDON_AREAS,
        locations: List[str] = CODES_LONDON_AREA_ALL,
        z: List[float] = None,
        style: MapboxStyle = MapboxStyle.CARTO_POSITRON,
        access_token: str = None,
        colorscale: Union[str, List[str]] = "hot"):

        assert geojson is not None, 'Please provide file path to the GeoJSON file'
        assert locations is not None, 'Please provide the list of locations'
        assert z is not None, 'Please provide the list of z-values'
        if style == MapboxStyle.DARK:
            assert access_token is not None, 'Access token has to be ' + \
                                            'provided for dark mapbox tiles'

        self.geojson_path = geojson
        with open(geojson) as json_file:
            self.geojson = json.load(json_file)

        self.fig = go.Figure(
            go.Choroplethmapbox(
                geojson=self.geojson,
                locations=locations,
                z=z,
                colorscale=colorscale,
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

        # TODO: Dynamically get the center?
        lat = 51.509865
        lon = -0.118092

        self.fig.update_layout(
            mapbox_style = self.style.value,
            mapbox_zoom = zoom,
            mapbox_center_lat = lat,
            mapbox_center_lon = lon,
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
