from app.sentiment_extractor import SentimentExtractor
from pandas import read_excel
import os

extractor = SentimentExtractor()
script_dir = os.path.dirname(__file__)
data = read_excel(script_dir + '/datasets/Tripadvisor Review Part1.xlsx')

feature_count = 0

for index, review in data.iterrows():
    feature_value = extractor.extract_feature(review, 'unsafe', -1)

    data.loc[data.index[index], 'feature_value'] = feature_value

    if data.at[index, 'feature_value'] != 0:
        feature_count += 1
        print("%d: %d %d" % (index, feature_count, data.at[index, 'feature_value']))

print('Found %d features from %d rows' % (feature_count, index))
