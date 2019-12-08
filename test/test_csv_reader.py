import unittest
from app.file.csv_reader import CsvReader
import os

script_dir = os.path.dirname(__file__)

class TestCsvReader(unittest.TestCase):

    def test_read_valid_csv(self):
        reader = CsvReader()
        file = script_dir + '/_files/2019-10-hampshire-street.csv'

        result = reader.read_csv(file)
        self.assertEqual(100, len(result))
        self.assertIn('Crime ID', result[0])

if __name__ == '__main__':
    unittest.main()