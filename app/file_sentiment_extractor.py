from app.sentiment_extractor import SentimentExtractor
from app.sentiment_feature import SentimentFeature

from app.file.utils import get_absolute_path
import pandas
import os

class FileSentimentExtractor:

    FEATURES = {
        SentimentFeature(
            'unsafe',
            ['unsafe'],
            -1
        ),
        SentimentFeature(
            'positive',
            ['positive', 'good', 'nice', 'great', 'wonderful', 'perfect'],
            1
        ),
        SentimentFeature(
            'crime',
            [
                'crime',
                'arson',
                'assault',
                'bribe',
                'burglar',
                'fraud',
                'homicide',
                'manslaughter', 
                'murder',
                'rape',
                'robbery',
                'shoplift',
                'trespassing',
                'gang'
            ],
            -1
        )
    }

    def process_file(self, file_path, save, output_file):
        """
        Extract sentiment features from file

        Keyword arguments:

        file_path -- Excel file path, absolute or relative to caller
        save -- If set, feature is saved to the file
        """
        if output_file is None:
            output_file = file_path

        file_path = get_absolute_path(file_path)

        if not os.path.isfile(file_path):
            print ("%s is not a valid file path" % file_path)
            return

        if not file_path.endswith('.xlsx'):
            print ("Not a valid Excel file")
            return

        print("Reading file " + file_path)
        data = pandas.read_excel(file_path)
        self.extract_all_words(data)

        if save:
            print("Saving features to file " + output_file)
            data.to_excel(output_file)
    
    def extract_all_words(self, data: pandas.DataFrame):
        """
        Extract all sentiment features for given DataFrame
        """
        for feature in self.FEATURES:
            self.extract_feature(data, feature)

    def extract_feature(self, data: pandas.DataFrame, feature: SentimentFeature):
        """
        Extract feature for all rows in given DataFrame
        """
        feature_name = 'feature_word_' + feature.name
        print("Extract sentiment feature for %s with words %s" % (feature_name, feature.words))

        feature_count = 0
        feature_total_value = 0

        extractor = SentimentExtractor()

        for index, review in data.iterrows():
            feature_value = extractor.extract_feature(review, feature.words, -1)
            
            if feature_value != 0:
                feature_count += 1
                feature_total_value += abs(feature_value)

            data.loc[data.index[index], feature_name] = feature_value

        print('Found %d features of %s from %d rows' % (feature_total_value, feature_name, index))