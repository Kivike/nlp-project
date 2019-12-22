from app.address_to_coordinate import AddressExtractor
from pandas import read_excel
import os

extractor = AddressExtractor()
script_dir = os.path.dirname(__file__)
data = read_excel(script_dir + '/datasets/Tripadvisor Review Part1.xlsx')