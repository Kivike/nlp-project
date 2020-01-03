from area import area
import json
import os
import concurrent.futures
import multiprocessing as mp
from typing import List, Any, Tuple
from shapely.geometry import shape, Point
import pandas as pd
import numpy as np
from app.map.constants import GJSON_LONDON_SECTORS
from app.file.utils import read_csv_directory
from app.time.period import Period

CRIME_DATA_DIR = os.path.join(os.path.dirname(__file__), 'datasets/metropolitan-street')
# HOTEL_DATA_DIR = os.path.join(os.path.dirname(__file__), 'datasets/Hotel_reviews_NLP')
HOTEL_DATA_INPUT = os.path.join(os.path.dirname(__file__), 'datasets/tripadvisor_output.xlsx')
OUT_DIR = os.path.join(os.path.dirname(__file__), 'datasets/out/')
FINAL_DATA_OUTPUT = 'final_data_avg.csv' # Use average values in the final output, thus _avg ending
SECTORIZED_HOTEL_DATA = 'hotel_reviews_sectorized.csv'
SECTORIZED_CRIME_DATA = 'crimes_sectorized.csv'
CPU_COUNT = mp.cpu_count()
FEATURE_COLUMNS = [
    # 'feature_word_unsafe',
    'sentiment_unsafe',
    'sentiment_crime',
    'sentiment_positive',
    'sentiment_sum'
]

with open(GJSON_LONDON_SECTORS) as json_file:
    geojson = json.load(json_file)

sectors = [ { 'shape': shape(feature['geometry']), 'id': feature['id'] } for feature in geojson['features'] ]

def identify(x) -> str:
    """Grab the ID of GeoJSON feature.
    
    Arguments:

        x -- GeoJSON feature object
    
    Returns:

        str -- The identifier of the feature
    """
    return x['id']

def chunck_it(seq: List[Any], num: int) -> List[List[Any]]:
    """Chunk a list into multiple lists. Sourced from Stackoverflow:
    https://stackoverflow.com/questions/2130016/splitting-a-list-into-n-parts-of-approximately-equal-length
    
    Arguments:

        seq {List[Any]} -- The original sequence

        num {int} -- Number of chunks
    
    Returns:
        List[List[Any]] -- The original sequence in chunks
    """
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg
    
    return out

def sectorize_zip(x) -> str:
    """Grab the post code sector out of ZIP address that is in form of `XX(X) X(XX)`.
    
    Arguments:

        x -- Hotel review data row
    
    Returns:

        str -- The formed sector
    """
    # Split the parts of post code
    parts = x['ZIP'].split()
    # Concatenate as district + sector number
    return parts[0] + (parts[1][0] if len(parts) > 1 else '')

def sectorize_coordinates(coordinates: List[str]) -> Tuple[dict, List[str]]:
    """Sectorize given coordinates based on globally declared sectors.
    
    Arguments:

        coordinates {List[str]} -- The list of coordinates in form of 'Latitude,Longitude'
    
    Returns:

        Tuple[dict, List[str]] -- Dictionary containing mappings of given coordinates and
        their sectors, and a list of coordinates that don't have sector mapping

    """
    sector_map = {}
    missing_sector = []
    pid = os.getpid()
    counter = 0
    print('PID {} accepting {} coordinates'.format(pid, len(coordinates)))
    for coord in coordinates:
        if counter > 0 and counter % 1000 == 0:
            print('PID {}: Iterating at {}'.format(pid, counter))
        counter += 1
        lat, lon = coord.split(',')
        point = Point(float(lon), float(lat))
        found = False
        for polygon in sectors:
            if polygon['shape'].contains(point):
                identifier = polygon['id']
                sector_map[coord] = identifier
                found = True
                break
        if not found:
            missing_sector.append(coord)
    
    print('PID {} finishing'.format(pid))
    return sector_map, missing_sector

def main():

    #########################
    # Step 1: Read hotel data
    #########################
    print('Loading hotel data...')
    period = Period()

    hotel_data = pd.read_excel(HOTEL_DATA_INPUT) # type: pd.DataFrame
    # Drop rows with empty ZIP codes
    hotel_data['ZIP'].replace('', np.nan, inplace = True)
    hotel_data.dropna(subset=['ZIP'], inplace = True)
    columns = [
        'Hotel Name',
        'Hotel Address',
        'City',
        'ZIP',
        'Review Title',
        'Review Content',
        'Review Date'
    ] + FEATURE_COLUMNS
    hotel_data = hotel_data[columns]
    period.end()
    print('Hotel data loaded in {}, {} rows\n'.format(period, len(hotel_data)))
    #########################
    # Step 2: Read crime data
    #########################
    print('Loading crime data...')
    period = Period()
    crime_data = read_csv_directory(
        CRIME_DATA_DIR,
        columns = ['Latitude', 'Longitude']
    )

    # Drop rows with empty locations
    crime_data = crime_data.dropna(subset=['Latitude', 'Longitude'])
    period.end()
    print('Crime data loaded in {}, {} rows\n'.format(period, len(crime_data)))

    ##############################
    # Step 3: Sectorize hotel data
    ##############################
    print('Sectorizing hotel data...')
    period = Period()

    hotel_data['sector'] = hotel_data.apply(sectorize_zip, axis=1)

    period.end()
    print('Sectorized hotel data in {}\n'.format(period))

    filename = OUT_DIR + SECTORIZED_HOTEL_DATA
    hotel_data.to_csv(filename)
    print('Saved the sectorized hotel data into {}'.format(filename))

    ##############################
    # Step 4: Sectorize crime data
    ##############################
    print('Sectorizing crime data...')
    period = Period()

    step1 = Period()
    crime_data['Coordinates'] = crime_data.apply(lambda x: '{}, {}'.format(x['Latitude'], x['Longitude']), axis=1)
    coordinates = crime_data.Coordinates.unique()
    step1.end()
    print('Counted unique coordinates ({}) in {}'.format(len(coordinates), step1))

    step2 = Period()

    num_processes = max(CPU_COUNT, 2)
    sector_map_all = {}
    missing_sector_all = []
    print('Launching {} procesesses...'.format(num_processes))
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
        chunked_coordinates = chunck_it(coordinates, num_processes)
        for sector_map, missing_sector in executor.map(sectorize_coordinates, chunked_coordinates):
            missing_sector_all = missing_sector_all + missing_sector
            sector_map_all = {**sector_map_all, **sector_map}
    
    step2.end()
    print(
        'Mapped unique coordinates to sectors in {}, {} coordinates missing sector'.format(
            step2,
            len(missing_sector_all)
        )
    )
    step3 = Period()
    crime_data['sector'] = crime_data.apply(
        lambda x: sector_map_all[x['Coordinates']] if x['Coordinates'] in sector_map_all else None,
        axis=1
    )
    step3.end()
    print('Mapped crime data into sectors in {}'.format(step3))

    period.end()
    print('Sectorized crime data in {}\n'.format(period))

    filename = OUT_DIR + SECTORIZED_CRIME_DATA
    crime_data.to_csv(filename)
    print('Saved sectorized crime data to {}\n'.format(filename))

    ###########################################
    # Step 5: Calculate areas for sectors (m^2)
    ###########################################
    print('Calculating areas (m^2) for sectors...')
    period = Period()
    areas = {}
    for feature in geojson['features']:
        areas[feature['id']] = area(feature['geometry'])

    period.end()
    print('Calculated areas in {}\n'.format(period))

    ######################
    # Step 6: Combine data
    ######################
    print('Combining data into a DataFrame...')
    period = Period()

    # Group Hotel data based on sector
    columns = [
        'sector'
    ] + FEATURE_COLUMNS
    hotel_data = hotel_data[columns]
    hotel_data.sort_values(by = ['sector'])
    hgb = hotel_data.groupby('sector') # type: pd.DataFrame

    counts = hgb.size().to_frame(name = 'review_count')

    # The final data
    df = (counts
        .join(hgb.agg({ 'sentiment_unsafe': 'mean' }))
        .join(hgb.agg({ 'sentiment_crime': 'mean' }))
        .join(hgb.agg({ 'sentiment_positive': 'mean' }))
        .join(hgb.agg({ 'sentiment_sum': 'mean' }))
        .reset_index()) # type: pd.DataFrame

    # Add area per sector
    df['area'] = df.apply(
        lambda row: areas[row['sector']] if row['sector'] in areas else np.nan,
        axis = 1
    )

    # Group crime data based on sector
    crime_data = crime_data[['sector']]
    crime_data.sort_values(by = ['sector'])
    cgb = crime_data.groupby('sector') # type: pd.DataFrame

    counts = cgb.size().to_frame(name = 'crime_count').reset_index() # type: pd.DataFrame
    
    # Join the count of crimes per sector to the final data
    df = df.join(counts.set_index('sector'), on = 'sector')

    # Drop NaN values
    df.dropna(subset = ['area', 'crime_count', 'review_count'], inplace = True)

    period.end()
    print('Combined data in {}, {} rows\n'.format(period, len(df)))

    filename = OUT_DIR + FINAL_DATA_OUTPUT
    df.to_csv(filename)
    print('Saved the final output into {}'.format(filename))

if __name__ == '__main__':
    main()
