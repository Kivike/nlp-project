import unittest
import pandas as pd
from app.map.heat_map import HeatMap, MapboxStyle

class TestHeapMap(unittest.TestCase):

    def test_valid_constructor_arguments(self):
        """Test that the constructor validates the given arguments.
        """
        without_lat = pd.DataFrame(columns=[HeatMap.LON])
        without_lon = pd.DataFrame(columns=[HeatMap.LAT])
        valid_data = pd.DataFrame(columns=[HeatMap.LAT, HeatMap.LON])
        with self.assertRaises(AssertionError):
            HeatMap(without_lat)

        with self.assertRaises(AssertionError):
            HeatMap(without_lon)

        with self.assertRaises(AssertionError):
            # Check that dark mapbox style raises without access token
            HeatMap(valid_data, style = MapboxStyle.DARK)        

        # Verify that these are acceptable
        HeatMap(valid_data)
        HeatMap(valid_data, style = MapboxStyle.DARK, access_token = "mock")

if __name__ == '__main__':
    unittest.main()