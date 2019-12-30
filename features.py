import argparse
from app.file_sentiment_extractor import FileSentimentExtractor

"""
Example:
python features.py --hotel-data "datasets/Tripadvisor Review Part1.xlsx" --save
"""

parser = argparse.ArgumentParser()
#parser.add_argument('--crime-data', metavar='C', nargs='?')
parser.add_argument('--hotel-data', metavar='H', nargs='?')
parser.add_argument('--save', action='store', const=True, nargs='?')

args = parser.parse_args()

output_file = args.save if args.save else False

if args.hotel_data:
    sent_ext = FileSentimentExtractor()
    sent_ext.process_file(args.hotel_data, output_file)
else:
    print("Nothing to do")
    