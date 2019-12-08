import unittest
from app.file.xlsx_reader import XlsxReader
import os

script_dir = os.path.dirname(__file__)

class TestXlsxReader(unittest.TestCase):

    def test_read_valid_xlsx(self):
        reader = XlsxReader()
        file = script_dir + '/_files/short_tripadvisor_part1.xlsx'
        
        result = reader.read_xlsx(file)
        self.assertEqual(171, len(result))
        self.assertIn('City', result[0])

if __name__ == '__main__':
    unittest.main()