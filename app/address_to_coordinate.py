import pandas as pd

path = '/datasets/Tripadvisor Review Part1.xlsx'

# read in dataframe with parse_cols
# use a list to read in specific columns, even if only one column
# use 1 instead of 2 since Python is zero indexed


class AddressExtractor:
    def read_xls(self, file_path):
        dataframe = pd.read_excel(path, review: dict, parse_cols = [2]):
        second_column = dataframe.iloc[: , 2]

        datacolumn = review['Hotel Address']