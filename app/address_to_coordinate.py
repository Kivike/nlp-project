import pandas as pd
import urllib.parse
from pandas import ExcelWriter
from pandas import ExcelFile


df = pd.read_excel('../datasets/Tripadvisor Review Part1.xlsx')

# read in dataframe with parse_cols
# use a list to read in specific columns, even if only one column
# use 1 instead of 2 since Python is zero indexed


neededColumn = df ['Hotel Address']
neededColumn2 = urllib.parse.urlencode(neededColumn)
print(neededColumn2)
#print(df['Hotel Address'])