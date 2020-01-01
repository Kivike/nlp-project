from app.sentiment_extractor import SentimentExtractor
from app.sentiment_feature import SentimentFeature
from app.file.utils import read_csv_directory, get_absolute_path
import pandas
import os

class FileSentimentExtractor:

    FEATURES = {
        SentimentFeature(
            'sentiment_unsafe',
            ['unsafe'],
            -1
        ),
        SentimentFeature(
            'sentiment_positive',
            ['positive', 'good', 'nice', 'great', 'wonderful', 'perfect'],
            1
        ),
        SentimentFeature(
            'sentiment_crime',
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

    FEATURE_SUM = 'sentiment_sum'
    
    def process_file(self, file_path, output_file):
        """
        Extract sentiment features from file

        Keyword arguments:

        file_path -- Excel file path, absolute or relative to caller
        save -- If set, feature is saved to the file
        """
        if output_file is True:
            output_file = file_path

        file_path = get_absolute_path(file_path)

        if os.path.isfile(file_path):
            print("Reading file " + file_path)
            data = pandas.read_excel(file_path)

        elif os.path.isdir(file_path):
            data = read_csv_directory(file_path, filetype = 'xlsx')
        else:
            print ("%s is not a valid file path" % file_path)
            return

        self.extract_all_words(data)
        self.sum_features(data)

        if output_file:
            print("Saving features to file " + output_file)
            data.to_excel(output_file)
    
    def extract_all_words(self, data: pandas.DataFrame):
        """
        Extract all sentiment features for given DataFrame
        """
        for feature in self.FEATURES:
            self.extract_feature(data, feature)

    def sum_features(self, data: pandas.DataFrame):
        """
        For each row, sum sentiment feature values and add it as a new column
        """
        print('Summing sentiment features to column ' + self.FEATURE_SUM)
        
        for index, review in data.iterrows():
            feature_sum = 0

            for feature in self.FEATURES:
                feature_sum += data.loc[data.index[index], feature.name]

            data.loc[data.index[index], self.FEATURE_SUM] = feature_sum

    def extract_feature(self, data: pandas.DataFrame, feature: SentimentFeature):
        """
        Extract feature for all rows in given DataFrame
        """
        print("Extract sentiment feature for %s with words %s" % (feature.name, feature.words))

        feature_count = 0
        feature_total_value = 0

        extractor = SentimentExtractor()

        for index, review in data.iterrows():
            feature_value = extractor.extract_feature(review, feature.words, -1)
            
            if feature_value != 0:
                feature_count += 1
                feature_total_value += abs(feature_value)

            data.loc[data.index[index], feature.name] = feature_value

        print('Found %d features of %s from %d rows' % (feature_total_value, feature.name, index))