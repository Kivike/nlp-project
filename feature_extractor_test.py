from app.feature_extractor import FeatureExtractor
from pandas import read_excel
import os

extractor = FeatureExtractor()
script_dir = os.path.dirname(__file__)
data = read_excel(script_dir + '/datasets/Tripadvisor Review Part1.xlsx')

feature_count = 0
low_star = 0
for index, review in data.iterrows():
    feature_value = extractor.extract_features(review)

    data.loc[data.index[index], 'feature_value'] = feature_value

    if data.at[index, 'feature_value'] > 0:
        feature_count += 1
        print(str(index) + " " + str(feature_count))

    if data.at[index, 'Review Stars'] <= 2:
        low_star += 1

print(index)
print (low_star)