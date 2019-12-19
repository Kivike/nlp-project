import argparse
from file_sentiment_extractor import FileSentimentExtractor

parser = argparse.ArgumentParser()
parser.add_argument('--crime-data', metavar='C', nargs='?')
parser.add_argument('--hotel-data', metavar='H', nargs='?')
parser.add_argument('--save', action='store_true')

args = parser.parse_args()
print(args)

save_to_file = args.save if args.save else False

if args.hotel_data and not args.crime_data:
    sent_ext = FileSentimentExtractor()
    sent_ext.process_file(args.hotel_data, save_to_file)
elif not args.hotel_data and args.crime_data:
    #TODO: Draw heatmap