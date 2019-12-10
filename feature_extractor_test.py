from app.feature_extractor import FeatureExtractor
from pandas import read_excel
import os

extractor = FeatureExtractor()
script_dir = os.path.dirname(__file__)
data = read_excel(script_dir + '/datasets/Tripadvisor Review Part1.xlsx')

feature_count = 0
for index, review in data.iterrows():
    feature_value = extractor.extractFeatures(review)

    data.loc[data.index[index], 'feature_value'] = feature_value

    if data.at[index, 'feature_value'] > 0:
        feature_count += 1
        print(str(index) + " " + str(feature_count))

print(index)