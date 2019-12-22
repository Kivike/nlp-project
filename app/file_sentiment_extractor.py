from app.sentiment_extractor import SentimentExtractor
from app.file.utils import get_absolute_path
import pandas
import os

class FileSentimentExtractor:

    def process_file(self, file_path, save):
        """
        Extract sentiment features from file

        Keyword arguments:

        file_path -- Excel file path, absolute or relative to caller
        save -- If set, feature is saved to the file
        """
        file_path = get_absolute_path(file_path)

        if not os.path.isfile(file_path):
            print ("%s is not a valid file path" % file_path)
            return

        if not file_path.endswith('.xlsx'):
            print ("Not a valid Excel file")
            return

        print("Reading file " + file_path)
        data = pandas.read_excel(file_path)
        self.extract_file_word(data, 'unsafe')

        if save:
            print("Saving features to file")
            data.to_excel(file_path)
    
    def extract_file_word(self, data: pandas.DataFrame, word: str):
        print("Extract sentiment feature for word " + word)
        feature_name = 'feature_word_' + word

        extractor = SentimentExtractor()
        feature_count = 0

        for index, review in data.iterrows():
            feature_value = extractor.extract_feature(review, word, -1)
            data.loc[data.index[index], feature_name] = feature_value

            if data.at[index, feature_name] != 0:
                feature_count += 1
                print("%d: %d %d" % (index, feature_count, data.at[index, feature_name]))

        print('Found %d features from %d rows' % (feature_count, index))
