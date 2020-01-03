from area import area
import json
import os
import concurrent.futures
import multiprocessing as mp
from typing import List, Any, Tuple
from shapely.geometry import shape, Point
import pandas as pd
from app.map.constants import GJSON_LONDON_SECTORS
from app.file.utils import read_csv_directory
from app.time.period import Period

CRIME_DATA_DIR = 'datasets/metropolitan-street'
HOTEL_DATA_DIR = 'datasets/Hotel_reviews_NLP'
CPU_COUNT = mp.cpu_count()
FINAL_DATA_OUTPUT = 'output.csv'

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
    return parts[0] + parts[1][0]

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

    hotel_data = read_csv_directory(
        HOTEL_DATA_DIR,
        filelimit = 1,
        filetype = 'xlsx'
    )

    # Drop rows with empty ZIP codes
    hotel_data = hotel_data.dropna(subset=['ZIP'])
    period.end()
    print('Hotel data loaded in {}, {} rows\n'.format(period, len(hotel_data)))

    #########################
    # Step 2: Read crime data
    #########################
    print('Loading crime data...')
    period = Period()
    crime_data = read_csv_directory(
        CRIME_DATA_DIR,
        filelimit=2
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

    #####################################
    # Step 5: Calculate areas for sectors
    #####################################
    print('Calculating areas for sectors...')
    period = Period()
    areas = [
        { 'area': area(feature['geometry']), 'id': feature['id'] } for feature in geojson['features']
    ]
    period.end()
    print('Calculated areas in {}'.format(period))

    ######################
    # Step 6: Combine data
    ######################
    print('Combining data into a DataFrame...')
    period = Period()

    df = hotel_data['sector', 'Review Stars'].groupby(by = 'sector').agg(['sum', 'count'])

    print(df)

    period.end()
    print('Combined data in {}'.format(period))

    


if __name__ == '__main__':
    main()
